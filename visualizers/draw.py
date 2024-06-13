import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    # Path to the dataset file
    dataset_file = 'preprocessed_data/Darina/dataset_1/kalman_filtered_emg_data.csv'
    # Read the dataset into a pandas DataFrame without a header
    df = pd.read_csv(dataset_file, header=None)

    # Print the first few rows to inspect the data
    print(df.head())

    # Assuming the EMG data starts from the first column and goes onward
    # Rename the columns to reflect EMG channels (e.g., 'emg1', 'emg2', etc.)
    num_columns = df.shape[1]
    column_names = [f'emg{i+1}' for i in range(num_columns)]
    df.columns = column_names

    # Print the columns of the DataFrame to confirm
    print("Columns in the dataset:", df.columns)

    # Assuming we are interested in all EMG channels for analysis
    # Combine all columns into a single series for processing
    emg_signal = df.values.flatten()

    # Define the noise segment (for simplicity, using the first 100 samples as noise)
    noise_segment = emg_signal[:100]
    signal_segment = emg_signal

    # Function to calculate SNR
    def calculate_snr(signal, noise):
        signal_power = np.mean(signal**2)
        noise_power = np.mean(noise**2)
        snr = 10 * np.log10(signal_power / noise_power)
        return snr

    # Calculate SNR
    snr = calculate_snr(signal_segment, noise_segment)
    print(f'SNR: {snr:.2f} dB')

    # Visualize the EMG data
    plt.figure(figsize=(12, 6))
    plt.plot(emg_signal, label='Raw EMG Signal')
    plt.title('Raw EMG Signal')
    plt.xlabel('Sample Number')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()