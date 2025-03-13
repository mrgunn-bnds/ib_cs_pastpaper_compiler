import os
import fitz  # PyMuPDF
from config_loader import config  # Import config as a Python dict

# Load Paths Settings
input_dir = config["renamed_dir"]
output_dir = config["cleaned_dir"]

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define removal rules
REMOVE_PATTERNS_OTHERS = ["Aucune partie", "Blank page", "without the authorization of the IB"]
KEEP_ONLY_OPTION_D = "Option D"  # Paper 2 & Paper 2 Marking Schemes

# Function to determine file type
def determine_file_type(filename):
    """Returns 'paper2', 'paper2_markscheme', or 'other' based on filename."""
    if "_Paper_2_" in filename and "_markscheme" in filename:
        return "paper2_markscheme"
    elif "_Paper_2_" in filename:
        return "paper2"
    else:
        return "other"  # Default for all other papers

# Function to clean PDFs
def clean_pdf(input_path, output_path):
    """Keeps or removes pages based on document type rules."""
    doc = fitz.open(input_path)
    clean_doc = fitz.open()
    file_type = determine_file_type(os.path.basename(input_path))

    found_option_d = False  # Track when we find "Option D" in Paper 2 Marking Schemes

    for page_num in range(len(doc)):
        text = doc[page_num].get_text("text")

        # Paper 2: Keep only pages that mention "Option D"
        if file_type == "paper2" and KEEP_ONLY_OPTION_D not in text:
            print(f"🗑 Removing page {page_num + 1} from {os.path.basename(input_path)} (Paper 2, No Option D)")
            continue  # Skip this page

        # Paper 2 Marking Schemes: Skip pages until "Option D" is found, then keep everything after that
        if file_type == "paper2_markscheme":
            if not found_option_d:
                if KEEP_ONLY_OPTION_D in text:
                    found_option_d = True  # Found "Option D", now include all pages
                else:
                    print(f"🗑 Skipping page {page_num + 1} from {os.path.basename(input_path)} (Paper 2 Markscheme, Before Option D)")
                    continue  # Skip pages until "Option D" appears

        # Other Papers: Remove pages containing unwanted text
        if file_type == "other" and any(pattern in text for pattern in REMOVE_PATTERNS_OTHERS):
            print(f"🗑 Removing page {page_num + 1} from {os.path.basename(input_path)} (Other Paper, Unwanted Text)")
            continue  # Skip this page

        # Keep page if no patterns matched
        clean_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

    # Save cleaned PDF
    if len(clean_doc) > 0:
        clean_doc.save(output_path)
        print(f"✅ Cleaned PDF saved: {output_path}")
    else:
        print(f"⚠ Skipped {os.path.basename(input_path)} (all pages removed)")

    doc.close()
    clean_doc.close()

# Process all PDFs in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        clean_pdf(input_path, output_path)
print(f"✅ Done cleaned files saved: {output_dir}")
