# Extract Clerk

An OCR pipeline that turns **scanned court yearbooks into structured CSV data**. It splits multi-page PDFs, runs OCR over each page, reassembles the text, and then parses out records for *clerks* and *judges* into separate tables.

Built for historical legal directories where the source material only exists as page scans and the interesting data — names, terms, appointments — is locked inside them.

## Pipeline

```
data/textbooks/*.pdf
   │
   ├─ 1. make_folder      one output folder per source document
   ├─ 2. split_pdf        multi-page PDF → single-page PDFs
   ├─ 3. convert_files    OCR each page via pytesseract → .txt
   ├─ 4. concat_files     reassemble pages into one text file per book
   └─ 5. extract_data     parse records → *_clerk.csv, *_judge.csv
   │
   ▼
data/extract_books/<book>/
   ├─ <book>.txt
   ├─ <book>_clerk.csv
   └─ <book>_judge.csv
```

Each stage writes to disk, so a failed run can be resumed by rerunning from the stage that broke rather than re-OCRing everything.

## Repository layout

```
src/
  main.py                 Pipeline entry point — runs all five stages in order
  config.py               Resolves INPUT_DIR / OUTPUT_DIR, creates them if absent
  convert/
    scan.py               PDF page → text via OCR
  extract/
    clerk.py              Clerk record parser
    judge.py              Judge record parser
  utils/
    file_operations.py    Folder creation, PDF splitting, concatenation
    pdf_operations.py     PDF-level helpers
    text_processing.py    Text normalisation and cleanup
  data/
    textbooks/            Input — place source PDFs here
    extract_books/        Output — generated text and CSVs
setup.sh                  Installs system and Python dependencies
```

## Prerequisites

Extract Clerk shells out to **Tesseract**, which is a system package rather than a Python one:

```bash
# macOS
brew install tesseract poppler

# Debian / Ubuntu
sudo apt-get install tesseract-ocr poppler-utils
```

Python 3.8 or higher is required.

## Installation

```bash
git clone https://github.com/amir0135/extract_clerk.git
cd extract_clerk

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Alternatively, `./setup.sh` performs the same steps.

## Usage

Drop the PDFs you want to process into `src/data/textbooks/`, then run the pipeline from the repository root:

```bash
python -m src.main
```

Results appear under `src/data/extract_books/`, one folder per source document.

> Run as a module (`python -m src.main`) rather than `python src/main.py` — the imports are package-relative.

## Output format

For each source document the pipeline emits two CSVs:

| File | Contents |
|---|---|
| `<book>_clerk.csv` | Clerk records extracted from the OCR text |
| `<book>_judge.csv` | Judge records extracted from the OCR text |

The intermediate `<book>.txt` is kept so extraction rules can be re-tuned and rerun without repeating OCR.

## Notes on accuracy

OCR quality on historical scans varies with print quality and skew. `src/utils/text_processing.py` holds the normalisation rules; if a particular volume parses badly, that is usually the right place to adjust before touching the extractors.

## Tech stack

Python · pytesseract · pandas · PyPDF

## License

MIT — see [LICENSE](LICENSE).
