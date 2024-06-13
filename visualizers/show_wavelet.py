import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():

    # Define the names and datasets
    male_names = ['Adam', 'Franek', 'Kajtek', 'Slawek']
    female_names = ['Darina', 'Gabi', 'Kasia', 'Misia']
    datasets = ['dataset_1', 'dataset_2', 'dataset_3']

    # Initialize empty lists to store all wavelet transform data and frequencies
    male_wavelet_data = []
    female_wavelet_data = []
    male_frequencies = []
    female_frequencies = []

    # Function to read and append wavelet transform data
    def read_wavelet_transform_data(name, dataset, gender):
        folder_path = f'/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/preprocessed_data/{name}/{dataset}/features'
        wavelet_file_path = os.path.join(folder_path, 'Wavelet Transform.csv')
        frequencies_file_path = os.path.join(folder_path, 'Wavelet Transform_frequencies.csv')
        
        # Read Wavelet Transform data
        wavelet_data = pd.read_csv(wavelet_file_path, header=None, on_bad_lines='skip').values.flatten()
        
        # Read Wavelet Transform frequencies
        frequencies = pd.read_csv(frequencies_file_path, header=None, on_bad_lines='skip').values.flatten()
        
        # Append the data and frequencies to the respective lists
        if gender == 'male':
            male_wavelet_data.append(wavelet_data)
            male_frequencies.append(frequencies)
        else:
            female_wavelet_data.append(wavelet_data)
            female_frequencies.append(frequencies)

    # Loop through all male names and datasets to accumulate the data
    for name in male_names:
        for dataset in datasets:
            read_wavelet_transform_data(name, dataset, 'male')

    # Loop through all female names and datasets to accumulate the data
    for name in female_names:
        for dataset in datasets:
            read_wavelet_transform_data(name, dataset, 'female')

    # Concatenate the accumulated data arrays
    male_wavelet_data = np.concatenate(male_wavelet_data)
    male_frequencies = np.concatenate(male_frequencies)
    female_wavelet_data = np.concatenate(female_wavelet_data)
    female_frequencies = np.concatenate(female_frequencies)

    # Print the dimensions of the concatenated arrays
    print("Shape of male_wavelet_data:", male_wavelet_data.shape)
    print("Shape of male_frequencies:", male_frequencies.shape)
    print("Shape of female_wavelet_data:", female_wavelet_data.shape)
    print("Shape of female_frequencies:", female_frequencies.shape)

    # Reshape the wavelet data to match the length of frequencies
    num_male_frequencies = len(male_frequencies) // len(male_names) // len(datasets)
    male_wavelet_data = np.reshape(male_wavelet_data, (num_male_frequencies, -1))

    num_female_frequencies = len(female_frequencies) // len(female_names) // len(datasets)
    female_wavelet_data = np.reshape(female_wavelet_data, (num_female_frequencies, -1))

    # Print the new dimensions of wavelet_data after reshaping
    print("Shape of male_wavelet_data after reshaping:", male_wavelet_data.shape)
    print("Shape of female_wavelet_data after reshaping:", female_wavelet_data.shape)

    # Plot the combined wavelet transform data for males
    plt.figure(figsize=(10, 6))
    plt.imshow(male_wavelet_data, extent=[0, male_wavelet_data.shape[1], male_frequencies[-1], male_frequencies[0]], aspect='auto', cmap='viridis')
    plt.colorbar(label='Amplitude')
    plt.title('Combined Wavelet Transform (Males)')
    plt.xlabel('Time Samples')
    plt.ylabel('Frequency')
    plt.show()

    # Plot the combined wavelet transform data for females
    plt.figure(figsize=(10, 6))
    plt.imshow(female_wavelet_data, extent=[0, female_wavelet_data.shape[1], female_frequencies[-1], female_frequencies[0]], aspect='auto', cmap='viridis')
    plt.colorbar(label='Amplitude')
    plt.title('Combined Wavelet Transform (Females)')
    plt.xlabel('Time Samples')
    plt.ylabel('Frequency')
    plt.show()

if __name__ == '__main__':
    main()