from typing import DefaultDict
from scipy.io import loadmat
import os
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt


# Define the base path and the folder names
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


# dict_keys(['__header__', '__version__', '__globals__', 'emg', 'acc', 'stimulus', 'glove', 'subject',
# 'exercise', 'repetition', 'restimulus', 'rerepetition', 'age', 'circumference', 'frequency', 'gender', 'height', 'weight', 'laterality', 'sensor'])

print(male_data)
male_data_div = np.array
for x in male_data:
    for y in x['emg'][8:]:
        male_data_div
        






