import os
from src.config import INPUT_DIR, OUTPUT_DIR
from src.utils.file_operations import make_folder, split_pdf, convert_files, concat_files, extract_data

def main():
    # Step 1: Create folders for the extracted data
    folder_list = make_folder(INPUT_DIR, OUTPUT_DIR)
    
    # Step 2: Filter out non-PDF folders from the folder list
    folder_list = [folder for folder in folder_list if not folder.endswith('.pdf')]
    
    # Step 3: Sort the folder list to ensure consistent processing order
    folder_list.sort()
    
    # Step 4: Split PDF files into individual pages (if needed)
    split_pdf(INPUT_DIR, folder_list)
    
    # Step 5: Convert scanned PDF pages to text
    convert_files(OUTPUT_DIR, folder_list)
    
    # Step 6: Concatenate the extracted text files
    concat_files(OUTPUT_DIR, OUTPUT_DIR, folder_list)
    
    # Step 7: Extract data from the concatenated text files
    extract_data(OUTPUT_DIR, folder_list)

if __name__ == "__main__":
    main()
