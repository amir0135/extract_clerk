from os import name
import numpy as np
import pandas as pd

'''
    This module consists some general functions that are used in the other modules
'''

def flat(list):
    return [item for sublist in list for item in sublist]

#extract index for places in text we are interessted in
def extract_ind(lst, item):
    return [i for i, x in enumerate(lst) if item in x]

#### returns index of last element in list #####
def last_index(lst):
    last_ind = []
    for i in range(len(lst)):
        last_ind.append(len(lst[i])-1)
    return last_ind


def clean_text(data):
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




    def index_order(data, start, end_ind, item):
        #Delete unecessary index of the word 'Chambers' since this appear in places we are not interested in
        start_ind = []
        for i in range(len(start)):
            if not item in data[start[i]]:
                start_ind.append(start[i]) 

        end_new = []
        end_new1 = []
        for i in start_ind:
            for j in end_ind:
                if j>i:
                    end_new.append(j)
                    break
        if len(start_ind) > len(end_new):
            #end_new.append(extract_ind(data, data[-1])[0])
            end_new.append(len(new_data)-1)
            end_new1.append(extract_ind(new_data, new_data[-1])[0])

        staff_data = []
        for j, k in zip(start_ind,end_new):
            staff_data.append(data[j:k])

        return staff_data

    # start = extract_ind(new_data, 'Staff')
    start = extract_ind(new_data, 'Chambers of')
    end = start[1:]
    #end.append(start[-1])
    staff_data_old = index_order(new_data, start, end, 'continued')

    staff_data = []
    for i in range(len(staff_data_old)):
        if staff_data_old[i][0].startswith('Chambers of'):
            staff_data.append(staff_data_old[i])
        elif not staff_data_old[i][0].startswith('Chambers of') and 'Chambers' in staff_data_old[i][0]:
            staff_data_old[i][0] = 'Chambers' + staff_data_old[i][0].split('Chambers')[-1]
            staff_data.append(staff_data_old[i])
        else:
            staff_data.append(staff_data_old[i-1]+ staff_data_old[i])

    def name_data_extraction(data):
        name_data = []
        for i in range(len(data)):
            if 'continued' in data[i][0]:
                pass
            if 'Chambers of' in data[i][0] and 'Judge' in data[i][0]:
                name_data.append(data[i][0].split("Judge")[1]) 
            elif 'Chambers of' in data[i][0] and 'Justice' in data[i][0]:
                name_data.append(data[i][0].split("Justice")[1])
        name_data = list(dict.fromkeys(name_data))
        return name_data
    
    save_name = name_data_extraction(staff_data) 
    test= []
    name_data = []
    for j in save_name:
        for i in range(len(staff_data)-1):
            if j in staff_data[i][0] and staff_data[i][0] not in staff_data[i+1][0]:
                test.append(staff_data[i])
                name_data.append(j)
                save_name = save_name[1:]
                break
            else:
                continue 

    return test, name_data

    #### exttracting names judge ###########


def word_ind(data, item):
    word_start = []
    for i in range(len(data)):
        if not [s for s in data[i] if item in s]:
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
                start_data.append(data[i][j:-1])
            else:
                start_data.append([data[i][j]])
        else:
            start_data.append(data[i][j:k])

        start_ny.append(' '.join(start_data[i]))

    return start_ny

