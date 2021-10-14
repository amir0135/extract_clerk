from new_extract import extract_clerk_info
from scan import convert_scanfiles
import os

''''
Run over all batch files
STEP 1: Write the directory to the folder for the pdf files
STEP 2: run the first part to convert from scan to txt
STEP 3: Run to extract information and save as a csv file

'''

# assign directory for batch files

directory = '/Users/Amira/Desktop/data_extract/test_files'

# def extract_all_clerk()
# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    ##checking if it is a file
    # if os.path.isfile(f) and filename.endswith('.pdf') :
    #     convert_scanfiles(f)

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if filename.endswith('.txt'):
        extract_clerk_info(f)

k = []