from typing import DefaultDict
from scipy.io import loadmat
import os
import numpy as np
import csv

def main():
    base_path = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/db'
    folder_names = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10']

    data_dict = DefaultDict(list)

    # Iterate over the folder names
    for folder_name in folder_names:
        # Initialize a list to store dataframes for each file in the folder
        dfs = []
        
        # Iterate over the files in the folder
        for file_name in os.listdir(os.path.join(base_path, folder_name)):
            if file_name.endswith('.mat'):
                # Construct the full path to the MATLAB data file
                file_path = os.path.join(base_path, folder_name, file_name)
                
                # Load the data from the MATLAB file
                mat_data = loadmat(file_path)
                
                # Convert MATLAB matrices to NumPy arrays
                for key, value in mat_data.items():
                    if isinstance(value, np.ndarray):
                        mat_data[key] = np.array(value)
                
                # Append the loaded data to the list of dataframes
                dfs.append(mat_data)
        
        # Add the list of dataframes to the dictionary
        data_dict[folder_name] = dfs


    male_data = []
    female_data = []
    for key, data in data_dict.items():
        for d in data:
            if d['gender'] == 'm':
                male_data.append(d)
            else:    
                female_data.append(d)



    dicti_m = {}
    dicti_f = {}
    for data in male_data:
        i = 0
        emg_matrix = data['emg']
        for row in emg_matrix:
            if i not in dicti_m:
                dicti_m[i] = []
            dicti_m[i].append(row[:8])
            i += 1


    for data in female_data:
        i = 0
        emg_matrix = data['emg']
        for row in emg_matrix:
            if i not in dicti_f:
                dicti_f[i] = []
            dicti_f[i].append(row[:8])
            i += 1


    columns = ['emg{}'.format(i) for i in range(1, len(dicti_m[1])*8 + 1)]

        # Unpack male_data['emg'] to male_data.csv
    with open('/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/raw_male_data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer = csv.writer(csvfile)
        for key, value in dicti_m.items():
            flattened_list = [item for sublist in value for item in sublist]
            writer.writerow(flattened_list)
            

    columns = ['emg{}'.format(i) for i in range(1, len(dicti_f[1])*8  + 1)]
                # Unpack female_data['emg'] to female_data.csv
    with open('/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/raw_female_data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer = csv.writer(csvfile)
        for key, value in dicti_f.items():
            flattened_list = [item for sublist in value for item in sublist]
            writer.writerow(flattened_list)
                

if __name__ == "__main__":
    main()
    print("Data extracted successfully.")