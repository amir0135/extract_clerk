

## Project Summary

Extract Clerk is a Python-based project designed to process and extract information from PDF files. The primary focus is on converting scanned PDF documents into text, and subsequently extracting structured data about clerks and judges. The project utilizes various libraries including `pytesseract` for OCR and `pandas` for data manipulation.

## Setup Instructions

### Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/amir0135/extract_clerk.git
    cd extract_clerk
    git checkout development
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Update the configuration paths in `src/config.py`:

```python
INPUT_DIR = '/path/to/your/textbooks'
OUTPUT_DIR = '/path/to/your/extract_books'
```

## Usage

### Running the Main Script

To run the main extraction process, execute the following command:

```bash
python src/main.py
```

This will:
1. Create necessary folders for the extracted data.
2. Split PDF files into individual pages if needed.
3. Convert scanned PDF pages to text.
4. Concatenate the extracted text files.
5. Extract data from the concatenated text files.

### Example

1. **Conversion of scanned PDFs to text:**

    The function `convert_scanfiles` in `src/convert/scan.py` converts each scanned PDF into a text file using OCR.

    ```python
    from convert.scan import convert_scanfiles

    converted_file = convert_scanfiles('/path/to/scanned.pdf')
    ```

2. **Extracting Clerk Information:**

    The function `extract_clerk_info` in `src/extract/clerk.py` processes the text files to extract information about clerks.

    ```python
    from extract.clerk import extract_clerk_info

    clerk_info_df = extract_clerk_info('/path/to/extracted_text.txt')
    print(clerk_info_df)
    ```

3. **Extracting Judge Information:**

    The function `extract_judge_info` in `src/extract/judge.py` processes the text files to extract information about judges.

    ```python
    from extract.judge import extract_judge_info

    judge_info_df = extract_judge_info('/path/to/extracted_text.txt')
    print(judge_info_df)
    ```

### Utilities

Several utility functions are provided in `src/utils` to assist with file operations and text processing:

- `file_operations.py`: Contains functions to create folders, split PDFs, convert files, concatenate files, and extract data.
- `pdf_operations.py`: Similar to `file_operations.py`, with a focus on PDF-specific operations.
- `text_processing.py`: Contains helper functions for text extraction and processing.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your improvements.

## License

This project is licensed under the MIT License.

