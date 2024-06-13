import os
import numpy as np
import pandas as pd
from scipy.signal import welch, stft
import pywt


def main():
    # Mean Absolute Value
    def mean_absolute_value(signal):
        return np.mean(np.abs(signal))

    # Root Mean Square
    def root_mean_square(signal):
        return np.sqrt(np.mean(signal**2))

    # Zero Crossing
    def zero_crossings(signal):
        zero_crossings = np.where(np.diff(np.signbit(signal)))[0]
        return len(zero_crossings)

    # Slope Sign Changes
    def slope_sign_changes(signal):
        diff_signal = np.diff(signal)
        slope_changes = np.where(np.diff(np.signbit(diff_signal)))[0]
        return len(slope_changes)

    # Waveform Length
    def waveform_length(signal):
        return np.sum(np.abs(np.diff(signal)))

    # Variance
    def variance(signal):
        return np.var(signal)

    # Mean Frequency
    def mean_frequency(signal, fs=1000):
        freqs, psd = welch(signal, fs)
        mean_freq = np.sum(freqs * psd) / np.sum(psd)
        return mean_freq

    # Median Frequency
    def median_frequency(signal, fs=1000):
        freqs, psd = welch(signal, fs)
        cumulative_sum = np.cumsum(psd)
        median_freq = freqs[np.where(cumulative_sum >= cumulative_sum[-1] / 2)[0][0]]
        return median_freq

    # Power Spectral Density
    def power_spectral_density(signal, fs=1000):
        freqs, psd = welch(signal, fs)
        return freqs, psd

    # Short-Time Fourier Transform (STFT)
    def short_time_fourier_transform(signal, fs=1000, nperseg=256):
        f, t, Zxx = stft(signal, fs, nperseg=nperseg)
        return f, t, Zxx

    # Wavelet Transform
    def wavelet_transform(signal):
        coeffs, freqs = pywt.cwt(signal, scales=np.arange(1, 128), wavelet='mexh')
        return coeffs, freqs

    names = ['Adam', 'Darina', 'Franek', 'Gabi', 'Kajtek', 'Kasia', 'Misia', 'Slawek']
    data_folder = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/preprocessed_data'

    # Dictionary to store features for each person and dataset
    features_dict = {}

    # Iterate over the names list
    for name in names:
        features_dict[name] = {}
        
        # Construct the path to the name folder
        name_folder = os.path.join(data_folder, name)
        
        # Iterate over the dataset folders
        for dataset in ['dataset_1', 'dataset_2', 'dataset_3']:
            # Construct the path to the emg_raw_data.csv file
            file_path = os.path.join(name_folder, dataset, 'kalman_filtered_emg_data.csv')
            
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(file_path, header=None, names=['amplitude'])
            
            # Extract the EMG signal
            emg_signal = df['amplitude'].values
            
            # Calculate features
            features = {
                'Mean Absolute Value': mean_absolute_value(emg_signal),
                'Root Mean Square': root_mean_square(emg_signal),
                'Zero Crossing': zero_crossings(emg_signal),
                'Slope Sign Changes': slope_sign_changes(emg_signal),
                'Waveform Length': waveform_length(emg_signal),
                'Variance': variance(emg_signal),
                'Mean Frequency': mean_frequency(emg_signal),
                'Median Frequency': median_frequency(emg_signal),
                'Power Spectral Density': power_spectral_density(emg_signal),
                'Short-Time Fourier Transform': short_time_fourier_transform(emg_signal),
                'Wavelet Transform': wavelet_transform(emg_signal)
            }
            
            # Store features in the dictionary
            features_dict[name][dataset] = features

    # Print the extracted features for verification
    for name, datasets in features_dict.items():
        print(f"Features for {name}:")
        for dataset, features in datasets.items():
            print(f"  Dataset: {dataset}")
            for feature_name, feature_value in features.items():
                print(f"    {feature_name}: {feature_value}")

    # Save the features as separate files in the features folder
    for name in names:
        name_folder = os.path.join(data_folder, name)
        for dataset in ['dataset_1', 'dataset_2', 'dataset_3']:
            dataset_folder = os.path.join(name_folder, dataset)
            features_folder = os.path.join(dataset_folder, 'features')
            os.makedirs(features_folder, exist_ok=True)
            
            # Save the features as separate files in the features folder
            features = features_dict[name][dataset]
            for feature_name, feature_value in features.items():
                if feature_name == 'Wavelet Transform':
                    # Use np.savetxt or pd.DataFrame.to_csv to save the array to a CSV file
                    file_path = os.path.join(features_folder, f"{feature_name}.csv")
                    np.savetxt(file_path, feature_value[0], delimiter=',')  # Save the wavelet coefficients
                    file_path = os.path.join(features_folder, f"{feature_name}_frequencies.csv")
                    np.savetxt(file_path, feature_value[1], delimiter=',')  # Save the frequencies
                elif feature_name == 'Short-Time Fourier Transform':
                    # Save Short-Time Fourier Transform as separate CSV files
                    file_path = os.path.join(features_folder, f"{feature_name}_frequencies.csv")
                    np.savetxt(file_path, feature_value[0], delimiter=',')
                    file_path = os.path.join(features_folder, f"{feature_name}_times.csv")
                    np.savetxt(file_path, feature_value[1], delimiter=',')
                    file_path = os.path.join(features_folder, f"{feature_name}_transform.csv")
                    np.savetxt(file_path, feature_value[2], delimiter=',')
                else:
                    # For other features, save as string
                    feature_file = os.path.join(features_folder, f"{feature_name}.csv")
                    with open(feature_file, 'w') as f:
                        f.write(str(feature_value))


if __name__ == "__main__":
    main()
    print("Feature extraction completed.")