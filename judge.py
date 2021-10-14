import numpy as np
import pandas as pd






'''
    This module cleans and extract the clerk information and connect them to their respective judge.
    Input: The clerk books in batches
    Output: CSV file

'''


def extract_judge_info(file):
    df = pd.DataFrame()

    with open(file, 'r') as f:
        data = [line.strip() for line in f]

#### clean text ########
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

    #### returns index of last element in list #####
    def last_index(lst):
        last_ind = []
        for i in range(len(lst)):
            last_ind.append(len(lst[i])-1)
        return last_ind


    def index_order(data, start, end_ind, item):
        #Delete unecessary index of the word 'Chambers' since this appear in places we are not interested in
        start_ind = []
        for i in range(len(start)):
            if not item in new_data[start[i]]:
                start_ind.append(start[i]) 

        end_new = []
        for i in start_ind:
            for j in end_ind:
                if j>i:
                    end_new.append(j)
                    break
        if len(start_ind) > len(end_new):
            end_new.append(extract_ind(new_data, new_data[-1])[0])

        staff_data = []
        for j, k in zip(start_ind,end_new):
            staff_data.append(data[j:k])

        return staff_data

    # start = extract_ind(new_data, 'Staff')
    start = extract_ind(new_data, 'Chambers of')
    end = start[1:]
    end.append(start[-1])
    staff_data_old = index_order(new_data, start, end, 'continued')

    staff_data = []
    for i in range(1, len(staff_data_old)-1):
        if staff_data_old[i][0].startswith('Chambers of'):
            staff_data.append(staff_data_old[i])
        else:
            staff_data.append(staff_data_old[i-1]+ staff_data_old[i])


    ##### exttracting names judge ###########
    name_data = []
    for i in range(len(staff_data)):
        if 'Chambers of' in staff_data[i][0] and 'Judge' in staff_data[i][0] and 'Staff' in staff_data[i]:
            name_data.append(staff_data[i][0].split("Judge")[1])
    ######## fill in index of words if exists or not ########

    test= []
    for i in range(len(staff_data)):
        if i == -1:
            break
        if staff_data[i][0] not in staff_data[i-1][0]:
            test.append(staff_data[i])

    test1= []   
    for i in range(len(test)):
        for j in name_data:
            if j in test[i][0]:
                test1.append(test[i])

        #### returns a list with index or N/A depending if information exists for each clerk ########
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

        return start_ny,



    #### the part that extracts list of the spefific coloumns####
    columns=['Education:','Began Service:','Appointed By:','Circuit Assignment:',
    'Government:','Judicial:','Legal Practice:','Current Memberships:']
    staff_data_ind = []
    for i in columns:
        staff_data_ind.append(word_ind(test1, i))


    data = []
    for j in range(len(staff_data_ind)):
        if j == len(staff_data_ind)-1:
            data.append(extract_information(test1, staff_data_ind[j], last_index(staff_data)))
        else:
            data.append(extract_information(test1, staff_data_ind[j], staff_data_ind[j+1]))

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
