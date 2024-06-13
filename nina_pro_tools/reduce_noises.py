import numpy as np
import pandas as pd


def main():
    # Define a smoothing function
    def smooth_data(data, window_size):
        smoothed_data = np.apply_along_axis(
            lambda x: np.convolve(x, np.ones(window_size) / window_size, mode='same'),
            axis=0,
            arr=data
        )
        return smoothed_data



    file_path = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/raw_female_data.csv'

    # Load the data using pandas
    data = pd.read_csv(file_path, header=None)

    # Round the data to a specified number of decimal places
    rounded_data = np.round(data, decimals=2)

    # Convert the rounded DataFrame back to a numpy array for smoothing
    rounded_data_np = rounded_data.to_numpy()


    # Apply smoothing
    window_size = 5  # You can adjust this parameter
    smoothed_data = smooth_data(rounded_data_np, window_size)

    # Convert the smoothed data back to a DataFrame
    smoothed_data_df = pd.DataFrame(smoothed_data)

    # Save the smoothed and rounded data back to a file
    output_file_path = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/noise_reduced_female_data.csv'
    smoothed_data_df.to_csv(output_file_path, index=False, header=False)

if __name__ == "__main__":
    main()
    print("Data noise reduction completed.")