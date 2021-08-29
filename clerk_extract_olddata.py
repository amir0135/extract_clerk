from os import name
from typing import Callable
from PIL.Image import new
from pandas.core.frame import DataFrame
import numpy as np
import pandas as pd
from numpy import append, empty, genfromtxt, info

'''
This file extracts clerk data from the older scanned files 
upload the txt file and run
'''

#### clean text ########
with open('batch1.txt', 'r') as f:
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

#### returns index of last element in list #####
def last_index(lst):
    last_ind = []
    for i in range(len(lst)):
        last_ind.append(len(lst[i])-1)
    return last_ind

def index_order(data, start_ind, end_ind):
#Delete unecessary index of the word 'Chambers' since this appear in places we are not interested in
    end_new = []
    for i in start_ind:
        for j in end_ind:
            if j>i:
                end_new.append(j)
                break
    end_new.append(extract_ind(new_data, new_data[-1])[0])


    staff_data = []
    for j, k in zip(start_ind,end_new):
        staff_data.append(data[j:k])

    return staff_data

start = extract_ind(new_data, 'Staff')
end = extract_ind(new_data, 'Chambers')
staff_data = index_order(new_data, start, end)

###### cleaning up and splitting up staff to each clerk#####
clerk_start = []
clerk_data = []
for i in range(len(staff_data)):
    clerk_start.append(extract_start_word(staff_data[i],'Law Clerk'))
    for j, k in zip(clerk_start[i], clerk_start[i][1:]):
        clerk_data.append(staff_data[i][j:k])
        if staff_data[i][k].startswith('Law Clerk') and k == clerk_start[i][-1]:
            if k == len(staff_data[i])-1:
                clerk_data.append([staff_data[i][k]])
            else:
                clerk_data.append(staff_data[i][k:-1])


##### exttracting names ###########
name_data = []
name_final = []
for i in range(len(clerk_data)):
    if '...' in clerk_data[i][0]:
        name_data.append(clerk_data[i][0].split("...")[0].split(' ')) ##### extract first line from clerk data and split
    else:
        name_data.append(clerk_data[i][0].split(' '))
    name_data[i] = name_data[i][2:] ######## delete 'law clerk' from names #######
    name_final.append(' '.join(name_data[i]))



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

    return start_ny,


columns=['Education:','Career:','Began service:','Term Expires:']
clerk_data_ind = []
for i in columns:
    clerk_data_ind.append(word_ind(clerk_data, i))


data = []
for j in range(len(clerk_data_ind)):
    if j == len(clerk_data_ind)-1:
        data.append(extract_information(clerk_data, clerk_data_ind[j], last_index(clerk_data)))
    else:
        data.append(extract_information(clerk_data, clerk_data_ind[j], clerk_data_ind[j+1]))

for i in range(len(columns)):
    for j in range(len(data[i][0])):
        if columns[i] in data[i][0][j]:
            data[i][0][j] = data[i][0][j].split(columns[i])[1]
        else: 
            continue




data.insert(0,[name_final])
columns.insert(0,'Name')
df = pd.DataFrame()


for i in range(len(data)):  
    # if data[]
    #     t.append(t.remove())
    df[columns[i]] = data[i][0]


df.to_csv('Clerk_data.csv', sep='\t', encoding='utf-8')

k = []