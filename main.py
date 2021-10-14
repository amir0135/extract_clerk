from new_extract import extract_clerk_info
from scan import convert_scanfiles
import os
from judge import extract_judge_info

''''
Run over all batch files
STEP 1: Write the directory to the folder for the pdf files
STEP 2: run the first part to convert from scan to txt
STEP 3: Run to extract information and save as a csv file

'''

def convert_files(dir):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        ##checking if it is a file
        if os.path.isfile(f) and filename.endswith('.pdf') :
            convert_scanfiles(f)
    return

def extract_data(dir):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if filename.endswith('.txt'):
            extract_clerk_info(f)
            extract_judge_info(f)
    return

####### STEP 1 #######
directory = '/Users/Amira/Desktop/data_extract/test_files'

####### STEP 2 ####### 
#run step 2 and 3 seperatly, since step 2 takes very long and only needs to be done once
convert_files(directory)

####### STEP 3 #######
extract_data(directory)