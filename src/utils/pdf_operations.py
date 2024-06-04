import os
import shutil
import numpy as np
from PyPDF2 import PdfFileReader, PdfFileWriter
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
                pdf_reader = PdfFileReader(open(pdf_path, 'rb'))
                for page in range(pdf_reader.numPages):
                    pdf_writer = PdfFileWriter()
                    pdf_writer.addPage(pdf_reader.getPage(page))
                    pdf_output = open(os.path.join(folder_path, f"{filename.split('.')[0]}_page{page}.pdf"), 'wb')
                    pdf_writer.write(pdf_output)
                    pdf_output.close()

def convert_files(directory, folder_list):
    folder_list.pop(0)  # Assumes the first item is not a relevant folder
    for folder_name in folder_list:
        folder_path = os.path.join(directory, folder_name)
        files = sorted(os.listdir(folder_path))
        for filename in files:
            for i in range(0, len(files), 2):
                if i == -1 or files[i].split('.')[0] == files[i + 1].split('.')[0]:
                    break
                convert_scanfiles(os.path.join(folder_path, filename))

def concat_files(directory, save_dir, folder_list):
    for folder_name in folder_list:
        folder_path = os.path.join(directory, folder_name)
        files = sorted(os.listdir(folder_path), key=lambda x: x.rsplit('page', 1)[1])
        files.sort(key=len)
        with open(os.path.join(save_dir, f"{folder_name}/{folder_name}.txt"), "wb") as output:
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
                extract_clerk_info(file_path)
                extract_judge_info(file_path)
