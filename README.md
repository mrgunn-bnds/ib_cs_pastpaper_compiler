# IB Past Paper Aggregator
This tool is used to turn a IB style folder full of Computer Science past papers into something more manageable for students:
- a single pdf containing all past papers in order, followed by their corresponding marking schemes optimized for my students learning:
  - There is only Option D in the paper 2 (Option A-C stripped)
  - There is no copyright notice pages to save space
  - There have been bookmarks added to facilitate navigation
- A json file of all questions and topics (for providing to a LLM for training)
- 
## Note
- Works on Windows only 
- It produces a rather large PDF that I then use Acrobat Pro DC to compress
- I am removing all but Option D questions from the Paper 2 question to streamline my students

## TODO
- make it so you dont have to change the variables
- make it so its one tool
- add code to compress the pdf similar to how adobe does it.

## Steps to use
| Script                               | Description               |
|--------------------------------------|---------------------------|
| 1. copy_and_rename_past_papers.py    | name the pdfs with date   |
| 2. past_paper_pdf_cleaner.py         | remove all but Option D   |
| 3. process_questions_to_make_json.py | make a json               |
| 4. merge_pdf.py | make the pdfs merged pdfs | 
| then compress the pdf with external tool |


