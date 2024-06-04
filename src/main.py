import os
from config import INPUT_DIR, OUTPUT_DIR
from utils.file_operations import make_folder, split_pdf, convert_files, concat_files, extract_data

def main():
    folder_list = make_folder(INPUT_DIR, OUTPUT_DIR)
    folder_list = [folder for folder in folder_list if not folder.endswith('.pdf')]
    folder_list.sort()
    extract_data(OUTPUT_DIR, folder_list)

if __name__ == "__main__":
    main()
