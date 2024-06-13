# Read Kalman filtered data

import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import resample
import numpy as np
from sklearn.linear_model import LinearRegression


def main():

    # read the data
    file_path = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/processed_data/kalman_filtered_data.csv'
    data = pd.read_csv(file_path, header=None)

    # Extract the data into a numpy array
    y = data.values.flatten()

    # Create a time array based on the sampling rate of 200 Hz
    sampling_rate = 200  # Hz
    time = np.arange(len(y)) / sampling_rate

    # Reshape the time array for linear regression
    time = time.reshape(-1, 1)

    # Perform linear regression
    model = LinearRegression()
    model.fit(time, y)
    trend = model.predict(time)

    # Plot the original data and the linear regression line
    plt.figure(figsize=(10, 6))
    plt.plot(time, y, label='Kalman Filtered Data')
    plt.plot(time, trend, label='Linear Regression', color='red', linewidth=2)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Filtered Data')
    plt.legend()
    plt.title('Kalman Filtered Data with Linear Regression')
    plt.show()



    from scipy.fft import fft, fftfreq

    # Number of samples
    N = len(y)
    # Compute the Fourier Transform
    yf = fft(y)
    xf = fftfreq(N, 1 / sampling_rate)

    # Plot the Fourier Transform
    plt.figure(figsize=(12, 6))
    plt.plot(xf, np.abs(yf))
    plt.xlim(0, 50)  # Limit to lower frequencies for better visualization
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Fourier Transform of Kalman Filtered Data')
    plt.show()



    # read the data
    file_path = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/processed_data/kalman_filtered_female_data.csv'
    data = pd.read_csv(file_path, header=None)

    # Extract the data into a numpy array
    y = data.values.flatten()

    # Create a time array based on the sampling rate of 200 Hz
    sampling_rate = 200  # Hz
    time = np.arange(len(y)) / sampling_rate

    # Reshape the time array for linear regression
    time = time.reshape(-1, 1)

    # Perform linear regression
    model = LinearRegression()
    model.fit(time, y)
    trend = model.predict(time)

    # Plot the original data and the linear regression line
    plt.figure(figsize=(10, 6))
    plt.plot(time, y, label='Kalman Filtered Data')
    plt.plot(time, trend, label='Linear Regression', color='red', linewidth=2)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Filtered Data')
    plt.legend()
    plt.title('Kalman Filtered Data with Linear Regression')
    plt.show()


    from scipy.fft import fft, fftfreq

    # Number of samples
    N = len(y)
    # Compute the Fourier Transform
    yf = fft(y)
    xf = fftfreq(N, 1 / sampling_rate)

    # Plot the Fourier Transform
    plt.figure(figsize=(12, 6))
    plt.plot(xf, np.abs(yf))
    plt.xlim(0, 50)  # Limit to lower frequencies for better visualization
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Fourier Transform of Kalman Filtered Data')
    plt.show()


if __name__ == '__main__':
    main()