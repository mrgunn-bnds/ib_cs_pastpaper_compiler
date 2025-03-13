import os
import re
import shutil
from config_loader import config  # Import config as a Python dict

# Load settings
source_dir = config["source_dir"]
output_renamed_dir = config["renamed_dir"]

# Regex pattern to match year and session from folder names
folder_pattern = re.compile(r"(\d{4})-(May|Nov)")

# Updated regex to handle variations (extra underscores)
file_pattern = re.compile(r"Computer_science_paper_?(\d)_?(TZ\d+_)?_?(HL|SL)_?(_markscheme)?\.pdf", re.IGNORECASE)

def copy_and_rename_files(base_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("\n=== Processing Folders ===")
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)

        # Debug: Print detected folders
        print(f"Checking folder: {folder}")

        # Match year and session (May/Nov)
        match = folder_pattern.match(folder)
        if match and os.path.isdir(folder_path):
            year, session = match.groups()
            print(f"Processing: {year}-{session}")

            print("\n=== Processing Files ===")
            for filename in os.listdir(folder_path):
                file_match = file_pattern.match(filename)

                if file_match:
                    paper_number, timezone, level, is_markscheme = file_match.groups()

                    # Format the new filename
                    new_filename = f"{year}-{session}_Paper_{paper_number}_{level}"
                    if timezone:
                        new_filename += f"_{timezone[:-1]}"  # Remove trailing "_"

                    if is_markscheme:
                        new_filename += "_markscheme"

                    new_filename += ".pdf"

                    # Full source and destination file paths
                    src_file_path = os.path.join(folder_path, filename)
                    dest_file_path = os.path.join(output_dir, new_filename)

                    # Copy file to output directory
                    try:
                        shutil.copy2(src_file_path, dest_file_path)
                        print(f"✅ Copied: {filename} → {new_filename}")
                    except Exception as e:
                        print(f"❌ Error copying {filename}: {e}")

                else:
                    print(f"⚠ Skipping: {filename} (Not matched)")
    print("Done! Double check",output_dir)

if __name__ == "__main__":
    copy_and_rename_files(source_dir, output_renamed_dir)
