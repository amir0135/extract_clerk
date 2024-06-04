def flat(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

def extract_ind(lst, item):
    return [i for i, x in enumerate(lst) if item in x]

def last_index(lst):
    return [len(sublist) - 1 for sublist in lst]

def clean_text(data):
    data = [line for line in data if line]
    
    start_indices = extract_ind(data, 'Chambers of')
    end_indices = start_indices[1:] + [len(data) - 1]
    
    staff_data = [data[start:end] for start, end in zip(start_indices, end_indices)]
    staff_data = [segment for segment in staff_data if segment[0].startswith('Chambers of')]
    
    name_data = [segment[0].split("Judge")[1] if "Judge" in segment[0] else segment[0].split("Justice")[1] for segment in staff_data]
    name_data = list(dict.fromkeys(name_data))
    
    return staff_data, name_data

def word_ind(data, item):
    word_start = [['N/A'] if not [s for s in segment if item in s] else extract_ind(segment, item) for segment in data]
    word_start = flat(word_start)
    return [indices[0] if len(indices) > 1 else indices for indices in word_start]

def extract_information(data, start_ind, end_ind):
    results = []
    for segment, start, end in zip(data, start_ind, end_ind):
        if start == 'N/A' and end == 'N/A':
            results.append('N/A')
        elif start == 'N/A':
            results.append('N/A')
        elif end == 'N/A':
            results.append(' '.join(segment[start:]))
        else:
            results.append(' '.join(segment[start:end]))
    return results
