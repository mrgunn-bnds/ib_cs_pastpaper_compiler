# IB Past Paper Aggregator
This tool is used to turn a IB style folder full of Computer Science past papers into something more manageable for students:
- a single pdf containing all past papers in order, followed by their corresponding marking schemes optimized for my students learning:
  - There is only Option D in the paper 2 (Option A-C stripped)
  - There is no copyright notice pages to save space
  - There have been bookmarks added to facilitate navigation
- A json file of all questions and topics (for providing to a LLM for training)

## What's not done
- The final produced merged pdfs are rather huge
  - Hence, I recommend you use Adobe PDF Pro DC and compress them
  
## Steps to use
1. edit config_loader.py to point to where all the HL pdfs are
2. run main
3. Enjoy the files
4. repeat step 1-3 for the SL