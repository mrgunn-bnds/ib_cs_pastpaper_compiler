import os
import fitz  # PyMuPDF
import json
import re
from config_loader import config  # Import the config dictionary

# Paths
input_dir = config["cleaned_dir"]
base_output_dir = config["output_dir"]
output_json = os.path.join(base_output_dir, "questions.json")

# Regex Patterns
QUESTION_PATTERN = re.compile(r"^\s*(\d+)\.\s+(.+)$")  # Matches "1. Describe..."
SUB_QUESTION_PATTERN = re.compile(r"^\(\s*([a-zA-Z])\s*\)\s*(.+)$")  # Matches "(a) Explain..."
SUB_SUB_QUESTION_PATTERN = re.compile(r"^\(\s*([i]+)\s*\)\s*(.+)$")  # Matches "(i) Describe..."
MAX_MARKS_PATTERN = re.compile(r"\[(\d+)\]")  # Matches "[X]" for max marks
PAGE_NUMBER_PATTERN = re.compile(r"^–\s*\d+\s*–$")  # Matches "- 2 -"
FOOTER_PATTERN = re.compile(r"^\d{4}-\d{4}.*")  # Matches footers like "2214-7011"
CONTINUATION_PATTERN = re.compile(r"This question continues on the following page|\(Question \d+ continued\)")  # Multi-page markers

# Function to extract exam metadata from filename
def extract_exam_info(filename):
    """Extracts year, session, and paper type from filenames like 2014-May_Paper_1_HL.pdf"""
    match = re.match(r"(\d{4})-(May|Nov)_Paper_(\d)_(HL|SL)(_markscheme)?\.pdf", filename)
    if match:
        year, session, paper, level, is_markscheme = match.groups()
        is_markscheme = bool(is_markscheme)  # True if it's a marking scheme
        return int(year), session, int(paper), level, is_markscheme
    return None

# Function to clean text (removes unwanted artifacts before storing in JSON)
def clean_text(line):
    if PAGE_NUMBER_PATTERN.match(line) or FOOTER_PATTERN.match(line):
        return ""  # Remove page numbers and footers
    return line.strip()

# Function to extract questions from PDFs
def extract_questions_from_pdf(pdf_path):
    """Extracts questions while properly handling multi-page content."""
    doc = fitz.open(pdf_path)
    questions = []
    current_question = None
    current_sub_question = []
    current_text = ""
    max_marks = None  # Store max marks per question
    previous_max_marks = None  # Used to catch misplaced marks
    is_continuing_question = False  # Flag for multi-page questions

    for page in doc:
        text = page.get_text("text", sort=True)  # Extract text in correct reading order
        lines = text.split("\n")

        found_question = False  # Flag to skip headers and page numbers until a question appears
        last_max_mark_found = False  # Flag to ignore text after last max mark

        for index, line in enumerate(lines):
            line = clean_text(line)  # Remove unwanted artifacts
            if not line:
                continue  # Skip empty or cleaned lines

            # If the last line of the previous page said "This question continues on the following page"
            # then append the next page's text to the previous question instead of treating it as a new one
            if is_continuing_question:
                current_text += " " + line
                is_continuing_question = False  # Reset flag
                continue

            # Skip all content at the top of a page until we find a question
            if not found_question:
                if QUESTION_PATTERN.match(line):  # Found a main question (e.g., "1. Describe...")
                    found_question = True
                else:
                    continue  # Skip this line since it's still in the header

            # Detect max marks like "[2]" and store separately
            marks_match = MAX_MARKS_PATTERN.search(line)
            if marks_match:
                previous_max_marks = int(marks_match.group(1))  # Extract number inside "[X]"
                line = line.replace(marks_match.group(0), "").strip()  # Remove from text
                last_max_mark_found = True  # Mark this as the last detected max marks

            # **Stop processing if we detect footer text after the last max mark**
            if last_max_mark_found and FOOTER_PATTERN.match(line):
                break  # Stop reading further lines after the last max mark

            # Detect if the page ends with a continuation note
            if CONTINUATION_PATTERN.match(line):
                is_continuing_question = True  # Mark that the next page continues this question
                continue  # Do not add this line to the text

            # Detect main questions like "1. Describe..."
            question_match = QUESTION_PATTERN.match(line)
            if question_match:
                if current_question is not None:
                    # Assign max marks (if found on the previous line)
                    if max_marks is None and previous_max_marks is not None:
                        max_marks = previous_max_marks

                    questions.append({
                        "Question_Number": current_question,
                        "Sub_Questions": current_sub_question,
                        "Text": current_text.strip(),
                        "Max_Marks": max_marks  # Assign max marks
                    })

                # Start a new question
                current_question = question_match.group(1)  # Question number
                current_text = question_match.group(2)  # Question text
                current_sub_question = []
                max_marks = None  # Reset for new question
                continue  # Move to next line

            # Detect sub-questions like "(a) Explain..."
            sub_question_match = SUB_QUESTION_PATTERN.match(line)
            if sub_question_match:
                if current_question is None:
                    print(f"⚠ Warning: Sub-question found before main question in {pdf_path}")
                    continue  # Skip invalid sub-questions

                current_sub_question.append({
                    "Sub_Question": sub_question_match.group(1),
                    "Text": sub_question_match.group(2),
                    "Max_Marks": previous_max_marks if previous_max_marks is not None else None
                })
                previous_max_marks = None  # Reset after assignment
                continue  # Move to next line

            # Detect sub-sub-questions like "(i) Describe..."
            sub_sub_question_match = SUB_SUB_QUESTION_PATTERN.match(line)
            if sub_sub_question_match:
                if current_sub_question:
                    current_sub_question[-1]["Text"] += "\n" + sub_sub_question_match.group(2)
                continue  # Move to next line

            # Append to sub-question if available, otherwise main question
            if current_sub_question:
                current_sub_question[-1]["Text"] += " " + line
            else:
                current_text += " " + line

    # Append last question
    if current_question is not None:
        # Assign max marks if missing
        if max_marks is None and previous_max_marks is not None:
            max_marks = previous_max_marks

        questions.append({
            "Question_Number": current_question,
            "Sub_Questions": current_sub_question,
            "Text": current_text.strip(),
            "Max_Marks": max_marks  # Assign max marks
        })

    doc.close()
    return questions

# Process all PDFs and create a structured dataset
data = {}

for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        file_path = os.path.join(input_dir, filename)
        exam_info = extract_exam_info(filename)

        if exam_info:
            year, session, paper, level, is_markscheme = exam_info
            key = f"{year}-{session}-Paper-{paper}-{level}"

            if not is_markscheme:
                # Extract questions
                questions = extract_questions_from_pdf(file_path)
                if key not in data:
                    data[key] = {"Year": year, "Session": session, "Paper": paper, "Level": level, "Questions": []}
                data[key]["Questions"].extend(questions)

# Save to JSON file
with open(output_json, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f"✅ JSON file saved: {output_json}")
