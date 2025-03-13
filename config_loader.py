import os

import os

config = {
    # source directory where PDFs are
    "source_dir": "C:\\Users\\dg\\Documents\Past Papers\\SL",

    # Step 1 : Pdfs are renamed here
    "renamed_dir": os.path.join(os.getenv('TEMP'), "renamed_pdfs"),

    # Step 2 : Directory where cleaned PDFs are stored
    "cleaned_dir": os.path.join(os.getenv('TEMP'), "output_renamed_pdfs_cleaned"),

    # Step 3: Base directory for merged output files (merged pdfs, json file)
    "output_dir": "C:\\Users\\dg\\Documents\\Past Papers\\SL\\Merged_Papers",
}