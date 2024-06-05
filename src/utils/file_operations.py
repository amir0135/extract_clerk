import os
import shutil
import numpy as np
from PyPDF2 import PdfReader, PdfWriter  # Update here
from src.convert.scan import convert_scanfiles
from src.extract.clerk import extract_clerk_info
from src.extract.judge import extract_judge_info

def make_folder(folder_dir, dir_save):
    folder_list = sorted(os.listdir(folder_dir))
    folder_list.pop(0)  # Assumes the first item is not a relevant folder
    for folder_name in folder_list:
        new_folder = os.path.join(dir_save, folder_name.split('.pdf')[0])
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
    return folder_list

def split_pdf(directory, folder_list):
    for folder_name in folder_list:
        folder_path = os.path.join(directory, folder_name)
        for filename in os.listdir(directory):
            if filename == f"{folder_name}.pdf":
                pdf_path = os.path.join(directory, filename)
                pdf_reader = PdfReader(open(pdf_path, 'rb'))  # Update here
                for page in range(len(pdf_reader.pages)):  # Update here
                    pdf_writer = PdfWriter()  # Update here
                    pdf_writer.add_page(pdf_reader.pages[page])  # Update here
                    pdf_output = open(os.path.join(folder_path, f"{filename.split('.')[0]}_page{page}.pdf"), 'wb')
                    pdf_writer.write(pdf_output)
                    pdf_output.close()

def convert_files(directory, folder_list):
    folder_list.pop(0)  # Assumes the first item is not a relevant folder
    for folder_name in folder_list:
        folder_path = os.path.join(directory, folder_name)
        files = sorted(os.listdir(folder_path))
        for filename in files:
            if filename.endswith('.pdf'):
                converted_file = convert_scanfiles(os.path.join(folder_path, filename))
                if converted_file is None:
                    print(f"Skipping file {filename} due to conversion error.")


def concat_files(directory, save_dir, folder_list):
    for folder_name in folder_list:
        folder_path = os.path.join(directory, folder_name)
        files = sorted(os.listdir(folder_path), key=lambda x: int(x.rsplit('page', 1)[1].split('.')[0]) if 'page' in x else float('inf'))
        files.sort(key=len)
        output_dir = os.path.join(save_dir, folder_name)
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f"{folder_name}.txt"), "wb") as output:
            for filename in files:
                if filename.endswith('.txt'):
                    with open(os.path.join(folder_path, filename), "rb") as file:
                        shutil.copyfileobj(file, output)


def extract_data(directory, folder_list):
    for folder_name in folder_list:
        folder_path = os.path.join(directory, folder_name)
        files = sorted(os.listdir(folder_path))
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)
                result = extract_clerk_info(file_path)
                if result is None:
                    print(f"Skipping file {file_path} due to lack of data.")
