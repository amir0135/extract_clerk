from os import name
from typing import Callable
from PIL.Image import new
from pandas.core.frame import DataFrame
import numpy as np
import pandas as pd
from numpy import append, empty, genfromtxt, info


'''
This file extracts Judge data from the older scanned files 
upload the txt file and run
'''

#### clean text ########
with open('output.txt', 'r') as f:
    data = [line.strip() for line in f]

lst_ind = []
for i in range(len(data)):
    if data[i] == '':
        lst_ind.append(False)
    else:
        lst_ind.append(True)

new_data = []
for i in range(len(data)):
    if lst_ind[i] == True:
        new_data.append(data[i])
    else:
        continue


#flatten list
def flat(list):
    return [item for sublist in list for item in sublist]

#extract index for places in text we are interessted in
def extract_ind(lst, item):
    return [i for i, x in enumerate(lst) if item in x]

def extract_start_word(lst, item):
    return [lst.index(l) for l in lst if l.startswith(item)]

def index_order(data, start_ind, end_ind):
#Delete unecessary index of the word 'Chambers' since this appear in places we are not interested in
    for i in start_ind:
        if 'continued' in data[i]:
            start_ind.pop(start_ind.index(i))
            
    #end_ind.append(extract_ind(data, data[-1])[0])

    staff_data = []
    for j, k in zip(start_ind,end_ind):
        staff_data.append(data[j:k])

    return staff_data
    
start = extract_ind(new_data, 'Chambers of Associate')
end = extract_ind(new_data, 'Staff')
staff_data = index_order(new_data, start, end)



##### exttracting names ###########
name_data = []
for i in range(len(staff_data)):
    if 'Justice' in staff_data[i][0] or 'Judge' in staff_data[i][0]:
        name_data.append(staff_data[i][0].split("Justice")[1]) 



######## fill in index of words if exists or not ########

    #### returns a list with index or N/A depending if information exists for each clerk ########
def word_ind(data, item):
    word_start = []
    test = []
    for i in range(len(data)):
        if [s for s in data[i] if item in s] == []:
            word_start.append(['N/A'])
        else:
            word_start.append(extract_ind(data[i],item))

        #flatten list
        if len(word_start[i]) > 1:
            word_start[i] = [word_start[i][0]] #delete if career pops up more times to have equal sizes
    word_start = flat(word_start)
    return word_start


''''
    takes in index from first word and index from last word-
    will extract information either from the first index to last index,
    only information from first index or only info from last index depending of existince of the
    words in each list

    input: data, start word index, end word index
    output: List of lists containing information from word or N/A

    example all information from the word 'education' all the way to the word 'career'

'''
def extract_information(data, start_ind, end_ind):
    start_data = []
    start_ny = []
    for i, j, k in zip(range(len(data)), start_ind, end_ind):
        #for i in range(len(data)):
        if j == 'N/A' and k == 'N/A':
            start_data.append('N/A')
        elif j == 'N/A':
            start_data.append('N/A')
        elif k == 'N/A':
            if j == len(data[i]):
                start_data.append(data[i][j])
            else:
                start_data.append(data[i][j:-1])
        else:
            start_data.append(data[i][j:k])

        start_ny.append(' '.join(start_data[i]))


    return start_ny


columns=['Education:','Began Service:','Appointed By:','Circuit Assignment:',
    'Government:','Judicial:','Legal Practice:','Current Memberships:']

staff_data_ind = []
for i in columns:
    staff_data_ind.append(word_ind(staff_data, i))

def last_index(lst):
    last_ind = []
    for i in range(len(lst)):
        last_ind.append(len(lst[i])-1)
    return last_ind

data = []
for j in range(len(staff_data_ind)):
    if j == len(staff_data_ind)-1:
        data.append(extract_information(staff_data, staff_data_ind[j], last_index(staff_data)))
    else:
        data.append(extract_information(staff_data, staff_data_ind[j], staff_data_ind[j+1]))


for i in range(len(columns)):
    for j in range(len(data[i])):
        if columns[i] in data[i][j]:
            data[i][j] = data[i][j].split(columns[i])[1]


data.insert(0,name_data)
columns.insert(0,'Name')
df = pd.DataFrame()

for i in range(len(data)):       
    df[columns[i]] = data[i]
        
df.to_csv('Judge_data.csv', sep='\t', encoding='utf-8')

k = []