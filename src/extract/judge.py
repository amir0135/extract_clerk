import pandas as pd
from src.utils import text_processing as lib

def extract_judge_info(file):
    with open(file, 'r') as f:
        data = [line.strip() for line in f]

    staff_data, name_data = lib.clean_text(data)

    judge_start_indices = [lib.extract_ind(segment, 'Staff') for segment in staff_data]
    judge_data = [segment[:indices[0]] if indices else 'N/A' for segment, indices in zip(staff_data, judge_start_indices)]
    
    columns = ['Education:', 'Began Service:', 'Appointed By:', 'Circuit Assignment:', 'Government:', 'Judicial:', 'Legal Practice:', 'Current Memberships:']
    staff_data_indices = [lib.word_ind(judge_data, col) for col in columns]

    data = [lib.extract_information(judge_data, start, end) for start, end in zip(staff_data_indices, staff_data_indices[1:] + [lib.last_index(judge_data)])]

    for i, col in enumerate(columns):
        data[i] = [entry.split(col)[1] if col in entry else entry for entry in data[i]]

    df = pd.DataFrame(data, columns=columns)
    df.insert(0, 'Judge', name_data)
    df.insert(0, 'id', df.groupby('Judge').ngroup())
    
    df.sort_values('id').to_csv(file.replace('.txt', '_judge.csv'), sep='\t', encoding='utf-8')
    return df
