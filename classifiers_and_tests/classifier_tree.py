import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report


def main():
    # Define the names and datasets
    names = ['Adam', 'Darina', 'Franek', 'Gabi', 'Kajtek', 'Kasia', 'Misia', 'Slawek']
    datasets = ['dataset_1', 'dataset_2', 'dataset_3']
    gender_labels = {'Adam': 'male', 'Darina': 'female', 'Franek': 'male', 'Gabi': 'female', 'Kajtek': 'male', 'Kasia': 'female', 'Misia': 'female', 'Slawek': 'male'}

    # Initialize empty lists to store all wavelet transform data and labels
    all_wavelet_data = []
    all_labels = []

    # Function to read wavelet transform data and label from a given path
    def read_wavelet_transform_data(folder, label):
        wavelet_file_path = os.path.join(folder, 'Wavelet Transform.csv')
        frequencies_file_path = os.path.join(folder, 'Wavelet Transform_frequencies.csv')
        wavelet_data = pd.read_csv(wavelet_file_path, header=None, on_bad_lines='skip').values.flatten()
        frequencies_data = pd.read_csv(frequencies_file_path, header=None, on_bad_lines='skip').values.flatten()
        combined_data = np.concatenate((wavelet_data, frequencies_data), axis=0)  # Combine wavelet and frequencies data

        
        return combined_data, label

    # Read data for individual names and datasets
    for name in names:
        for dataset in datasets:
            data_folder = f'/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/preprocessed_data/{name}/{dataset}/features'
            combined_data, label = read_wavelet_transform_data(data_folder, gender_labels[name])
            all_wavelet_data.append(combined_data)
            all_labels.append(label)

    # Find the maximum length of combined data arrays
    max_length = max(len(data) for data in all_wavelet_data)

    # Pad combined data arrays to have the same length
    padded_combined_data = [np.pad(data, (0, max_length - len(data)), 'constant') for data in all_wavelet_data]

    # Convert lists to numpy arrays
    X = np.array(padded_combined_data)
    y = np.array(all_labels)

    # Print the shape of the data
    print("Shape of X:", X.shape)
    print("Shape of y:", y.shape)

    # Check class distribution
    print("Class distribution:", pd.Series(y).value_counts())

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize and train the Random Forest classifier
    rf_clf = RandomForestClassifier(n_estimators=110, random_state=42)
    rf_clf.fit(X_train, y_train)

    # Predict on the test set
    y_pred = rf_clf.predict(X_test)

    # Evaluate the classifier
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Cross-validation score
    cv_scores = cross_val_score(rf_clf, X, y, cv=5)
    print("CV Average Score:", cv_scores.mean())

if __name__ == "__main__":
    main()
    print("Classifier Tree completed.")
