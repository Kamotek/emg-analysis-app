import os
import numpy as np
import pandas as pd
from filterpy.kalman import KalmanFilter


def main():
    def normalize(DataFrame):
        # substract 120 from each value
        return DataFrame - 120

    names = ['Adam', 'Darina', 'Franek', 'Gabi', 'Kajtek', 'Kasia', 'Misia', 'Slawek']



    # Specify the path to the preprocessed_data folder
    data_folder = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/preprocessed_data'

    # Iterate over the names list
    for name in names:
        # Construct the path to the name folder
        name_folder = os.path.join(data_folder, name)
        
        # Iterate over the dataset folders
        for dataset in ['dataset_1', 'dataset_2', 'dataset_3']:
            # Construct the path to the emg_raw_data.csv file
            file_path = os.path.join(name_folder, dataset, 'emg_raw_data.csv')
            
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(file_path)
            df = normalize(df)
            # Process the data as needed
            # apply a Kalman filter to the data

            # Define the Kalman filter
            kf = KalmanFilter(dim_x=2, dim_z=1)

            # Define the state transition matrix
            kf.F = np.array([[1, 1],
                            [0, 1]])
            
            # Define the observation matrix
            kf.H = np.array([[1, 0]])

            # Define the process noise covariance
            kf.Q = np.array([[0.001, 0],
                            [0, 0.001]])
            
            # Define the measurement noise covariance
            kf.R = 0.1

            # Define the initial state mean and covariance
            kf.x = np.array([0, 0])
            kf.P = np.eye(2)

            # Parse the data
            data = np.array(df)

            # Apply the Kalman filter to each data point
            filtered_data = []
            for observation in data:
                kf.predict()
                # Make sure observation is a scalar
                observation_scalar = observation[0]
                kf.update(observation_scalar)
                filtered_data.append(kf.x[0])

            # Write down the filtered data to a new csv file
            filtered_data_df = pd.DataFrame(filtered_data)
            output_file_path = os.path.join(name_folder, dataset, 'kalman_filtered_emg_data.csv')
            filtered_data_df.to_csv(output_file_path, index=False, header=False)


if __name__ == "__main__":
    main()
    print("Kalman filtering completed.")