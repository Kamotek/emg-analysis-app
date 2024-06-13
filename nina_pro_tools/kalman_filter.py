import pandas as pd
from filterpy.kalman import KalmanFilter
import numpy as np
def main():
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

    file_path = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/noise_reduced_female_data.csv'
    data = data = pd.read_csv(file_path, header=None)
    data = np.array(data)

    # Apply the Kalman filter to each data point
    # Apply the Kalman filter to each data point
    filtered_data = []
    for observation in data:
        kf.predict()
        # Make sure observation is a scalar
        observation_scalar = observation[0]  # Assuming observation is a 1D array
        kf.update(observation_scalar)
        filtered_data.append(kf.x[0])

    # Write down the filtered data to a new csv file

    filtered_data_df = pd.DataFrame(filtered_data)
    output_file_path = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/kalman_filtered_female_data.csv'
    filtered_data_df.to_csv(output_file_path, index=False, header=False)


if __name__ == "__main__":
    main()
    print("Kalman filtering completed.")