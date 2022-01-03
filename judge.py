from os import name
import numpy as np
import pandas as pd
import library as lib





'''
    This module cleans and extract the clerk information and connect them to their respective judge.
    Input: The clerk books in batches
    Output: CSV file

'''


def extract_judge_info(file):
    df = pd.DataFrame()

    with open(file, 'r') as f:
        data = [line.strip() for line in f]

    #### clean all text ########
    staff_data, name_data = lib.clean_text(data)
    
    
    judge_start = []
    for i in range(len(staff_data)):
        judge_start.append(lib.extract_ind(staff_data[i],'Staff'))


    ##### defining clerk data #######
    judge_data = []
    judge_start_new = []
    count = 0
    for i in range(len(judge_start)):
        if len(judge_start[i]) >= 2:
           judge_start_new.append([judge_start[i].pop(-1)])
        elif len(judge_start[i]) == 0:
            judge_start_new.append('N')
        else:
            judge_start_new.append(judge_start[i])
        
        
    judge_start_new = lib.flat(judge_start_new)
    for i in range(len(judge_start_new)):
        if judge_start_new[i] != 'N':
            judge_data.append(staff_data[i][:judge_start_new[i]])
        else:
            judge_data.append('N/A')
    
    
    
    
    
    
    
    
    
        
    #### the part that extracts list of the spefific coloumns####
    columns=['Education:','Began Service:','Appointed By:','Circuit Assignment:',
    'Government:','Judicial:','Legal Practice:','Current Memberships:']
    staff_data_ind = []
    for i in columns:
        staff_data_ind.append(lib.word_ind(judge_data, i))


    data = []
    for j in range(len(staff_data_ind)):
        if j == len(staff_data_ind)-1:
            data.append([lib.extract_information(judge_data, staff_data_ind[j], lib.last_index(staff_data))])
        else:
            data.append([lib.extract_information(judge_data, staff_data_ind[j], staff_data_ind[j+1])])
            
            

    ###### cleaning list by deleting coloumsname from data #####
    for i in range(len(columns)):
        for j in range(len(data[i][0])):
            if columns[i] == 'Current Memberships:' in data[i][0][j]:
                data[i][0][j] = data[i][0][j].split(columns[i])[1]
                if data[i][0][j].endswith('Staff') == False:
                    data[i][0][j] = data[i][0][j].split('Staff')[0] # cleaning up last row
            else:
                if columns[i] in data[i][0][j]:
                    data[i][0][j] = data[i][0][j].split(columns[i])[1]


    #### adding the name coloumn to the other coloumns
    columns.insert(0,'id')
    data.insert(1,[name_data])
    columns.insert(1,'Judge')

    for i in range(len(data)):  
        df[columns[i]] = data[i][0]
    df['id'] = df.groupby(['Judge']).ngroup()
    sorted_df = df.sort_values('id')
    #df = df.assign(id=(df['Name']).astype('category').cat.codes)
    sorted_df.to_csv(file.replace('.txt','_judge.csv'), sep='\t', encoding='utf-8')

    
    return sorted_df
