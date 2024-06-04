import pandas as pd
import src.utils.text_processing as lib

def extract_clerk_info(file):
    with open(file, 'r') as f:
        data = [line.strip() for line in f]

    staff_data, name_data = lib.clean_text(data)

    clerk_start_indices = [lib.extract_ind(segment, 'Staff') for segment in staff_data]
    clerk_data = [segment[start[0]:] if start else ['N/A'] for segment, start in zip(staff_data, clerk_start_indices)]
    
    clerk_ind = [lib.extract_ind(segment, 'Law Clerk') for segment in clerk_data]
    clerk = [segment[ind[0]:] if ind else ['N/A'] for segment, ind in zip(clerk_data, clerk_ind)]
    
    columns = ['Began Service:', 'Term Expires:', 'E-mail:', 'Education:', 'Career:']
    clerk_data_indices = [lib.word_ind(clerk, col) for col in columns]

    data = [lib.extract_information(clerk, start, end) for start, end in zip(clerk_data_indices, clerk_data_indices[1:] + [lib.last_index(clerk)])]

    for i, col in enumerate(columns):
        data[i] = [entry.split(col)[1] if col in entry else entry for entry in data[i]]

    df = pd.DataFrame(data, columns=columns)
    df.insert(0, 'Clerk', [segment[0] for segment in clerk])
    df.insert(0, 'Judge', name_data)
    df.insert(0, 'id', df.groupby('Judge').ngroup())

    df.sort_values('id').to_csv(file.replace('.txt', '_clerk.csv'), sep='\t', encoding='utf-8')
    return df
