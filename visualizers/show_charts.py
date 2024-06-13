import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import resample
import numpy as np


def main():
    # Parameters
    file_path = 'processed_data/noise_reduced_male_data.csv'
    chunk_size = 10000  # Adjust this based on your memory capacity
    fs = 200
    downsample_factor = 4  # Adjust this factor to reduce the data size

    # Function to process each chunk
    def process_chunk(chunk):
        data_flattened = chunk.values.flatten()
        data_downsampled = resample(data_flattened, len(data_flattened) // downsample_factor)
        return data_downsampled

    # Read and process data in chunks
    data_downsampled_list = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        data_downsampled = process_chunk(chunk)
        data_downsampled_list.append(data_downsampled)

    # Concatenate all downsampled data
    data_downsampled = np.concatenate(data_downsampled_list)

    # Create time axis
    time = np.linspace(0, len(data_downsampled) / fs, len(data_downsampled))

    # Plot the amplitude by time
    plt.figure(figsize=(10, 6))
    plt.plot(time, data_downsampled)
    plt.ylabel('Amplitude')
    plt.xlabel('Time [ms]')
    plt.title('Amplitude vs Time')
    plt.grid(True)
    plt.show()


    file_path = 'processed_data/noise_reduced_female_data.csv'
    chunk_size = 10000  # Adjust this based on your memory capacity
    fs = 200
    downsample_factor = 4  # Adjust this factor to reduce the data size

    # Function to process each chunk
    def process_chunk(chunk):
        data_flattened = chunk.values.flatten()
        data_downsampled = resample(data_flattened, len(data_flattened) // downsample_factor)
        return data_downsampled

    # Read and process data in chunks
    data_downsampled_list = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        data_downsampled = process_chunk(chunk)
        data_downsampled_list.append(data_downsampled)

    # Concatenate all downsampled data
    data_downsampled = np.concatenate(data_downsampled_list)

    # Create time axis
    time = np.linspace(0, len(data_downsampled) / fs, len(data_downsampled))

    # Plot the amplitude by time
    plt.figure(figsize=(10, 6))
    plt.plot(time, data_downsampled)
    plt.ylabel('Amplitude')
    plt.xlabel('Time [ms]')
    plt.title('Amplitude vs Time')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()