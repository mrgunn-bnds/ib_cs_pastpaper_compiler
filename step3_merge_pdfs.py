import os
import fitz  # PyMuPDF
import re
from config_loader import config  # Import the config reader

# Load settings
input_cleaned_dir = config["cleaned_dir"]
output_merged_dir = config["output_dir"]

# Ensure base_output_dir exists
os.makedirs(output_merged_dir, exist_ok=True)

# Define output paths using the base directory
output_paper1 = os.path.join(output_merged_dir, "IB_CS_Paper_1s.pdf")
output_paper2 = os.path.join(output_merged_dir, "IB_CS_Paper_2s.pdf")

# Sorting function to order by year and session
def extract_exam_info(filename):
    """Extracts year, session, and paper type from filenames like 2014-May_Paper_1_HL.pdf"""
    match = re.match(r"(\d{4})-(May|Nov)_Paper_(\d)_(HL|SL)(_markscheme)?\.pdf", filename)
    if match:
        year, session, paper, level, is_markscheme = match.groups()
        is_markscheme = 1 if is_markscheme else 0  # Ensure mark schemes come after the exam paper
        return int(year), session, int(paper), level, is_markscheme
    return (9999, "Z", 9, "ZZ", 9)  # Default for unknown formats (places them last)

# Get all cleaned PDFs and sort them
pdf_files = [f for f in os.listdir(input_cleaned_dir) if f.endswith(".pdf")]
pdf_files.sort(key=extract_exam_info)  # Sort by year, session, paper number, then mark scheme

# Separate PDFs into Paper 1 and Paper 2
paper1_files = [f for f in pdf_files if "_Paper_1_" in f]
paper2_files = [f for f in pdf_files if "_Paper_2_" in f]

# Function to merge PDFs and add precisely aligned bookmarks
def merge_papers(paper_files, output_pdf):
    """Merges PDFs and adds bookmarks for easy navigation, fixing the off-by-one issue."""
    merged_pdf = fitz.open()
    toc = []  # Table of Contents list for bookmarks

    print(f"\n🔄 Merging PDFs into {output_pdf}...")

    for filename in paper_files:
        file_path = os.path.join(input_cleaned_dir, filename)
        doc = fitz.open(file_path)

        # Extract metadata from filename
        year, session, paper, level, is_markscheme = extract_exam_info(filename)

        # Determine bookmark title
        if is_markscheme:
            bookmark_title = f"{year} {session} - Paper {paper} {level} (Marking Scheme)"
        else:
            bookmark_title = f"{year} {session} - Paper {paper} {level}"

        # Get the correct starting page number **before** inserting the new PDF
        start_page = merged_pdf.page_count + 1  # FIX: Add +1 to align with PDF readers

        # Add the document to the merged PDF
        merged_pdf.insert_pdf(doc)

        # Store bookmark info (now using the corrected start page)
        toc.append((1, bookmark_title, start_page))  # Level 1 bookmark

        print(f"✅ Added: {bookmark_title} (Page {start_page})")

    # Apply bookmarks (Table of Contents)
    merged_pdf.set_toc(toc)

    # Save merged PDF
    merged_pdf.save(output_pdf)
    merged_pdf.close()
    print(f"\n✅ Merged PDF saved as: {output_pdf}")

# Merge Paper 1s and Paper 2s separately
merge_papers(paper1_files, output_paper1)
merge_papers(paper2_files, output_paper2)
