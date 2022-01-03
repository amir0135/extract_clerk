from new_extract import extract_clerk_info
from scan import convert_scanfiles
import os
from judge import extract_judge_info
import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
import numpy as np
import shutil

'''
READ ME:

    This is the main program which loops over the pdf files and creates a folder for each batch file.

    This program consists of 4 files:
    scan.py - this is the file that reads the scanned files and converts them to txt files
    judge.py - this is the file that reads the txt files and extracts the judge information
    new_extract.py - this is the file that reads the txt files and extracts the clerk information

    main.py - this is the main file that runs the program and you have to insert the directory of the scanned files and the directory of where you want to save the files.
'''


def make_folder(folder_dir, dir_save):
    folder_list = os.listdir(folder_dir)
    folder_list = list(np.asarray(folder_list))
    folder_list.sort()
    folder_list.pop(0)
    for i in folder_list:
        if not os.path.exists(dir_save + '/' + i.split('.pdf')[0]):
            os.makedirs(dir_save + '/' + i.split('.pdf')[0])
    return folder_list

def split_pdf(directory, folder_list):
    for folder_name in folder_list:
        folder_path = directory + '/' + folder_name
        for filename in os.listdir(directory):
            if filename == folder_name + '.pdf':
                f = os.path.join(directory, filename)
                pdf_reader = PdfFileReader(open(f, 'rb'))
                for page in range(pdf_reader.numPages):
                    pdf_writer = PdfFileWriter()
                    pdf_writer.addPage(pdf_reader.getPage(page))
                    pdf_output = open(folder_path + '/' + '%s_page%s.pdf' % (filename.split('.')[0], page), 'wb')
                    pdf_writer.write(pdf_output)
                    pdf_output.close()
    return

def convert_files(dir, folder_list):
    folder_list.pop(0)
    for folder_name in folder_list:
        folder_path = dir + '/' + folder_name
        path = os.listdir(folder_path)
        path.sort()
        for filename in path:
            for i in range(0,len(path),2):
                if i == -1:
                    break
                elif path[i].split('.')[0] == path[i+1].split('.')[0]:
                    pass
                else:
                    f = os.path.join(folder_path, filename)
                    convert_scanfiles(f)
    return

def concatFiles(dir, save_dir, folder_list):
    for folder_name in folder_list:
        folder_path = dir + '/' + folder_name
        path = os.listdir(folder_path)
        path = sorted(path, key = lambda x: x.rsplit('page',1)[1])
        path.sort(key = len)
        with open(os.path.join(save_dir ,folder_name +'/' + folder_name + '.txt'), "wb") as fo:
            for filename in path:
                if filename.endswith('.txt'):
                    with open(os.path.join(folder_path, filename), "rb") as fi:
                        shutil.copyfileobj(fi, fo)
    return

def extract_data(dir, folder_list):
    for folder_name in folder_list:
        folder_path = dir + '/' + folder_name
        path = os.listdir(folder_path)
        path.sort()
        for filename in path:
            # if len([s for s in path if "csv" in s]) >= 2:
            #     break
            if filename.endswith('.txt'):
                f = os.path.join(folder_path, filename)
                extract_clerk_info(f)
                extract_judge_info(f)
            else:
                pass
    return


###### MAIN #########

#### uncomment the following lines to run the program

def main(dir, save_dir):
    # folder_list = make_folder(dir, dir)
    # new_folder_list = []
    # for i in folder_list:
    #     if not i.endswith('.pdf'):
    #         new_folder_list.append(i)
    # new_folder_list.sort()
    # split_pdf(dir, new_folder_list)
    # convert_files(dir, new_folder_list)

    folder_list = make_folder(dir, save_dir)
    new_folder_list = []
    for i in folder_list:
        if not i.endswith('.pdf'):
            new_folder_list.append(i)
    new_folder_list.sort()
    #concatFiles(dir, save_dir, new_folder_list)
    extract_data(save_dir, new_folder_list)
    return

''''

MAIN PROGRAM

Run over all batch files DOWN BELOW
STEP 1: Write the directory to the folder for the pdf files
    dir = folder with all the pdf files
    save_dir = folder to save the txt files
    uncomment everything in the main function

'''

dir = '/Users/Amira/Desktop/data_extract/textbooks'
save_dir = '/Users/Amira/Desktop/data_extract/extract_books'

main(dir, save_dir)