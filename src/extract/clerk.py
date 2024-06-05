import pandas as pd
from src.utils import text_processing as lib

def extract_clerk_info(file):
    with open(file, 'r') as f:
        data = [line.strip() for line in f]

    if not data:
        print(f"No data found in file {file}. Skipping.")
        return None

    # Print the raw data for debugging
    print(f"Raw data from file {file}:")
    print(data)

    staff_data, name_data = lib.clean_text(data)

    # Debugging print statements
    print(f"Staff data: {staff_data}")
    print(f"Name data: {name_data}")

    if not staff_data or not name_data:
        print(f"No relevant data found in file {file}. Skipping.")
        return None

    clerk_start_indices = [lib.extract_ind(segment, 'Staff') for segment in staff_data]
    clerk_data = [segment[start[0]:] if start else ['N/A'] for segment, start in zip(staff_data, clerk_start_indices)]

    clerk_ind = [lib.extract_ind(segment, 'Law Clerk') for segment in clerk_data]
    clerk = [segment[ind[0]:] if ind else ['N/A'] for segment, ind in zip(clerk_data, clerk_ind)]

    columns = ['Began Service:', 'Term Expires:', 'E-mail:', 'Education:', 'Career:']
    clerk_data_indices = [lib.word_ind(clerk, col) for col in columns]

    data = [lib.extract_information(clerk, start, end) for start, end in zip(clerk_data_indices, clerk_data_indices[1:] + [lib.last_index(clerk)])]

    for i, col in enumerate(columns):
        if not data[i]:  # Check if data list is empty
            data[i] = ['N/A'] * len(clerk)  # Fill with default values
        else:
            data[i] = [entry.split(col)[1] if col in entry else entry for entry in data[i]]

   
