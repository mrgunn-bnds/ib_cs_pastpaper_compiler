import subprocess
import sys

# List of scripts to run in order
scripts = ["step1_copy_and_rename_past_papers.py",
           "step2_past_paper_pdf_cleaner.py",
           "step3_merge_pdfs.py",
           "step4_process_questions_to_make_json.py"]

for script in scripts:
    print(f"\n🚀 Running {script}...\n" + "="*40)
    result = subprocess.run([sys.executable, script], capture_output=True, text=True, encoding="utf-8")

    # Print script output
    print(result.stdout)

    # Check for errors
    if result.returncode != 0:
        print(f"❌ Error in {script}:")
        print(result.stderr)
        break  # Stop execution if a script fails

print("\n✅ All steps completed!")