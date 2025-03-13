# 📘 IB Past Paper Aggregator

This tool helps organize **IB Computer Science past papers** into a more structured and student-friendly format.

## ✨ Features
- 📄 **Single PDF Output**: Merges all past papers into **one file** with structured bookmarks.
- ✅ **Optimized for Students**:
  - **Only Option D** included in Paper 2 (removes Options A-C).
  - 🚀 **Removes copyright pages** to save space.
  - 📌 **Bookmarks added** for easy navigation.
- 📝 **JSON Output**: Extracts **all questions and topics** into a structured JSON file for AI training or further processing.

---

## ⚠️ Known Issue
- 🚀 **The final merged PDFs are large**  
  - **Solution:** Use **Adobe PDF Pro DC** or another tool to compress them.

---

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/mrgunn-bnds/ib_cs_pastpaper_compiler.git
cd ib_cs_pastpaper_compiler
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Configure Input Paths
Edit `config_loader.py` and set the correct **input folder** for **HL** or **SL** past papers.

```python
config = {
    "cleaned_dir": "C:\Path\To\HL_Papers",
    "base_output_dir": "C:\Path\To\Output"
}
```

---

## 🚀 Usage
1. **Ensure `config_loader.py` is set up correctly.**
2. **Run the script** to generate the merged PDFs and JSON output:
   ```sh
   python main.py
   ```
3. **Check the output folder** for the processed files.
4. **Repeat steps 1-3** for **SL past papers** by changing `cleaned_dir`.

---

## 📂 Output Files
- 📄 `IB_CS_Paper_1s.pdf` (Merged Paper 1s)
- 📄 `IB_CS_Paper_2s.pdf` (Merged Paper 2s, **Option D only**)
- 📝 `questions.json` (Extracted topics & questions)

---

## 🛠 Troubleshooting
- **Dependencies not found?** Run:
  ```sh
  pip install -r requirements.txt
  ```
- **Unicode errors in Windows?** Run:
  ```sh
  chcp 65001
  ```
- **PDFs too big?** Use **Adobe PDF Pro DC** or another compression tool.

---

## 🏆 Contributing
Feel free to submit issues or pull requests!

---

## 📜 License
[MIT](LICENSE)
