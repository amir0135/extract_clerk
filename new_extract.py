from PIL.Image import new
import numpy as np
import pandas as pd
from numpy import append, empty, genfromtxt, info
import library as lib
'''
    This module cleans and extract the clerk information and connect them to their respective judge.
    Input: The clerk books in batches
    Output: CSV file

'''


def extract_clerk_info(file):
    df = pd.DataFrame()

    with open(file, 'r') as f:
        data = [line.strip() for line in f]


    ###### extract clean data and judges names ######
    staff_data, name_data = lib.clean_text(data)

    ###### cleaning up and splitting up staff to each clerk#####
    clerk_start = []
    for i in range(len(staff_data)):
        clerk_start.append(lib.extract_ind(staff_data[i],'Staff'))


    ##### defining clerk data #######
    clerk_old = []
    clerk_start_new = []
    count = 0
    for i in range(len(clerk_start)):
        if len(clerk_start[i]) >= 2:
           clerk_start_new.append([clerk_start[i].pop(-1)])
        elif len(clerk_start[i]) == 0:
            clerk_start_new.append('N')
        else:
            clerk_start_new.append(clerk_start[i])
        
    clerk_start_new = lib.flat(clerk_start_new)
    for i in range(len(clerk_start_new)):
        if clerk_start_new[i] != 'N':
            clerk_old.append(staff_data[i][clerk_start_new[i]:])
        else:
            clerk_old.append(['N/A'])
    
    ##### defining clerk data #######
    clerk_ind = []
    for i in range(len(clerk_old)):
        clerk_ind.append(lib.extract_ind(clerk_old[i],'Law Clerk'))

    clerk = []
    count = 0
    for i in range(len(clerk_ind)):
        if len(clerk_ind[i]) == 0:
            clerk.append(['N/A'])
            clerk[count].append(name_data[i])
            count+=1
        for j in range(len(clerk_ind[i])):
            if j == len(clerk_ind[i])-1:
                clerk.append(clerk_old[i][clerk_ind[i][j]:])
            else:
                clerk.append(clerk_old[i][clerk_ind[i][j]:clerk_ind[i][j+1]])
        
            clerk[count].append(name_data[i])
            count+=1
    clerk_data = []
    for i in clerk:
        if i not in clerk_data:
            clerk_data.append(i)



    ##### exttracting clerk names ###########

    delete_words = ['Career', 'Law Clerk']
    for j in range(len(delete_words)):
        for i in range(len(clerk_data)):
            if '...' in clerk_data[i][0]:
                clerk_data[i][0] = clerk_data[i][0].split('...')[0].split(' ')
                clerk_data[i][0] = ' '.join(clerk_data[i][0]) ##### extract first line from clerk data and split
            
            if delete_words[j] in clerk_data[i][0]:
                clerk_data[i][0] = clerk_data[i][0].split(delete_words[j])[1].split(' ')
            else:
                clerk_data[i][0] = clerk_data[i][0].split(' ')
            clerk_data[i][0] = ' '.join(clerk_data[i][0])

    name_final = []
    for i in range(len(clerk_data)):
        name_final.append(clerk_data[i][0])

    


    # ######## fill in index of words if exists or not ########

    #### the part that extracts list of the spefific coloumns####
    columns=['Began Service:','Term Expires:','E-mail:','Education:','Career:']
    clerk_data_ind = []
    for i in columns:
        clerk_data_ind.append(lib.word_ind(clerk_data, i))


    data = []
    for j in range(len(clerk_data_ind)):
        if j == len(clerk_data_ind)-1:
            data.append([lib.extract_information(clerk_data, clerk_data_ind[j], lib.last_index(clerk_data))])
        else:
            data.append([lib.extract_information(clerk_data, clerk_data_ind[j], clerk_data_ind[j+1])])

    ###### cleaning list by deleting coloumsname from data #####
    for i in range(len(columns)):
        for j in range(len(data[i][0])):
            if columns[i] == 'E-mail:' in data[i][0][j]:
                data[i][0][j] = data[i][0][j].split(columns[i])[1]
                if data[i][0][j].endswith('gov') == False:
                    data[i][0][j] = data[i][0][j].split('gov')[0]+'.gov' # cleaning up email list
            else:
                if columns[i] in data[i][0][j]:
                    data[i][0][j] = data[i][0][j].split(columns[i])[1]


    #### adding the name coloumn to the other coloumns
    data.insert(0,[name_final])
    columns.insert(0,'Clerk')


    ### adding the judges coloumn to the other columns
    judges = []
    for i in range(len(clerk_data)):
        judges.append(clerk_data[i][-1])

    data.insert(0,[judges])
    columns.insert(0,'Judge')

    
    
    ##### generating dataframes and converting to CSV file ####
    for i in range(len(data)):  
        df[columns[i]] = data[i][0]
    df['id'] = df.groupby(['Judge']).ngroup()
    first_column = df.pop('id')
    df.insert(0, 'id', first_column)
    sorted_df = df.sort_values('id')
    sorted_df.to_csv(file.replace('.txt','_clerk.csv'), sep='\t', encoding='utf-8')

    return sorted_df

#extract_clerk_info('test_files/testnew.txt')

