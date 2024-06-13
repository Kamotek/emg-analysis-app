import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline

def main():
    # Define the names and datasets
    names = ['Adam', 'Darina', 'Franek', 'Gabi', 'Kajtek', 'Kasia', 'Misia', 'Slawek']
    datasets = ['dataset_1', 'dataset_2', 'dataset_3']
    gender_labels = {'Adam': 'male', 'Darina': 'female', 'Franek': 'male', 'Gabi': 'female', 'Kajtek': 'male', 'Kasia': 'female', 'Misia': 'female', 'Slawek': 'male'}

    # Initialize empty lists to store all wavelet transform data and labels
    all_wavelet_data = []
    all_labels = []

    # Function to read wavelet transform data from a given path
    def read_wavelet_transform_data(folder):
        wavelet_file_path = os.path.join(folder, 'Wavelet Transform.csv')
        wavelet_data = pd.read_csv(wavelet_file_path, header=None, on_bad_lines='skip').values.flatten()
        return wavelet_data

    def read_wavelet_transform_freq_data(folder):
        wavelet_freq_file_path = os.path.join(folder, 'Wavelet Transform_frequencies.csv')
        wavelet_freq_data = pd.read_csv(wavelet_freq_file_path, header=None, on_bad_lines='skip').values.flatten()
        return wavelet_freq_data

    # Read data for individual names and datasets
    max_length = 0
    data_store = []

    for name in names:
        for dataset in datasets:
            data_folder = f'/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/preprocessed_data/{name}/{dataset}/features'
            try:
                wavelet_data = read_wavelet_transform_data(data_folder)
                wavelet_freq_data = read_wavelet_transform_freq_data(data_folder)

                # Combine the data
                combined_data = np.concatenate((wavelet_data, wavelet_freq_data))
                data_store.append((combined_data, gender_labels[name]))

                # Update max_length
                if len(combined_data) > max_length:
                    max_length = len(combined_data)
            except Exception as e:
                print(f"Skipping {name}-{dataset} due to error: {e}")
                continue

    # Pad data to make all records the same length
    for combined_data, label in data_store:
        padded_data = np.pad(combined_data, (0, max_length - len(combined_data)), 'constant')
        all_wavelet_data.append(padded_data)
        all_labels.append(label)

    # Convert lists to numpy arrays
    X = np.array(all_wavelet_data)
    y = np.array(all_labels)

    # Print the shape of the data
    print("Shape of X:", X.shape)
    print("Shape of y:", y.shape)

    # Check class distribution
    print("Class distribution:", pd.Series(y).value_counts())

    # Determine the maximum number of components for PCA
    max_components = min(X.shape[0], X.shape[1], 16)  # Ensure n_components is <= 16

    # Create a pipeline with StandardScaler, PCA, and Logistic Regression
    pipeline = make_pipeline(
        StandardScaler(),
        PCA(n_components=max_components),  # Adjust the number of components dynamically
        LogisticRegression(random_state=42)
    )

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Train the logistic regression model
    pipeline.fit(X_train, y_train)

    # Predict on the test set
    y_pred = pipeline.predict(X_test)

    # Evaluate the classifier
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Cross-validation score
    cv = StratifiedKFold(n_splits=6, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X, y, cv=cv)
    print("CV Average Score:", cv_scores.mean())

if __name__ == "__main__":
    main()
    print("Logistic regression classifier executed successfully.")
