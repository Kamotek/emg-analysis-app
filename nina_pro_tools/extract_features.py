import os
import numpy as np
import pandas as pd
from scipy.signal import welch, find_peaks
from scipy.fft import fft, fftfreq
import pywt

def main():
    # Feature calculation functions
    def mean_absolute_value(signal):
        return np.mean(np.abs(signal))

    def root_mean_square(signal):
        return np.sqrt(np.mean(signal**2))

    def zero_crossings(signal):
        zero_crossings = np.where(np.diff(np.signbit(signal)))[0]
        return len(zero_crossings)

    def slope_sign_changes(signal):
        diff_signal = np.diff(signal)
        slope_changes = np.where(np.diff(np.signbit(diff_signal)))[0]
        return len(slope_changes)

    def waveform_length(signal):
        return np.sum(np.abs(np.diff(signal)))

    def variance(signal):
        return np.var(signal)

    def mean_frequency(signal, fs=1000):
        freqs, psd = welch(signal, fs)
        mean_freq = np.sum(freqs * psd) / np.sum(psd)
        return mean_freq

    def median_frequency(signal, fs=1000):
        freqs, psd = welch(signal, fs)
        cumulative_sum = np.cumsum(psd)
        median_freq = freqs[np.where(cumulative_sum >= cumulative_sum[-1] / 2)[0][0]]
        return median_freq

    def power_spectral_density(signal, fs=1000):
        freqs, psd = welch(signal, fs)
        return freqs, psd

    def short_time_fourier_transform(signal, fs=1000, nperseg=256):
        from scipy.signal import stft
        f, t, Zxx = stft(signal, fs, nperseg=nperseg)
        return f, t, Zxx

    def wavelet_transform(signal):
        coeffs, freqs = pywt.cwt(signal, scales=np.arange(1, 128), wavelet='mexh')
        return coeffs, freqs

    # Path to the processed data folder
    data_folder = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/processed_data'

    # Files to process and their corresponding folders
    file_info = [
        ('kalman_filtered_data.csv', 'male'),
        ('kalman_filtered_female_data.csv', 'female')
    ]

    # Iterate over the files and process each one
    for file_name, gender_folder in file_info:
        # Construct the path to the file
        file_path = os.path.join(data_folder, file_name)
        
        if os.path.exists(file_path):
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(file_path, header=None)
            
            # Extract the EMG signal
            emg_signal = df[0].values
            
            # Calculate features
            features = {
                'Mean Absolute Value': [mean_absolute_value(emg_signal)],
                'Root Mean Square': [root_mean_square(emg_signal)],
                'Zero Crossings': [zero_crossings(emg_signal)],
                'Slope Sign Changes': [slope_sign_changes(emg_signal)],
                'Waveform Length': [waveform_length(emg_signal)],
                'Variance': [variance(emg_signal)],
                'Mean Frequency': [mean_frequency(emg_signal)],
                'Median Frequency': [median_frequency(emg_signal)],
            }
            
            # Calculate and handle multi-valued features
            freqs, psd = power_spectral_density(emg_signal)
            features['Power Spectral Density'] = psd
            features['Power Spectral Density Frequencies'] = freqs

            f, t, Zxx = short_time_fourier_transform(emg_signal)
            features['Short-Time Fourier Transform'] = Zxx
            features['Short-Time Fourier Transform Frequencies'] = f
            features['Short-Time Fourier Transform Times'] = t

            coeffs, freqs = wavelet_transform(emg_signal)
            features['Wavelet Transform'] = coeffs
            features['Wavelet Transform_frequencies'] = freqs
            
            # Create directory if it doesn't exist
            gender_folder_path = os.path.join(data_folder, gender_folder)
            if not os.path.exists(gender_folder_path):
                os.makedirs(gender_folder_path)
            
            # Save each feature in a separate CSV file
            for feature_name, feature_values in features.items():
                feature_file_path = os.path.join(gender_folder_path, feature_name + '.csv')
                
                # Handle multi-valued features
                feature_df = pd.DataFrame(feature_values)
        
                
                feature_df.to_csv(feature_file_path, index=False, header=False)

            print(f"Features saved in {gender_folder_path}")

if __name__ == "__main__":
    main()
    print("Feature extraction completed.")