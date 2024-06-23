import io
import os
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report
import yaml
import gzip
import pickle
from pathlib import Path

def main():
    # Define base directory
    base_dir = Path("assets/band")

    # Initialize empty lists to store all EMG data and labels
    all_emg_data = []
    all_labels = []

    max_length = 0
    data_store = []

    # Iterate over all subdirectories in base_dir
    for subdir in base_dir.rglob('*'):
        if subdir.is_dir():
            # Look for the kalman_filtered_emg_data.pkl.gz file
            emg_data_file = subdir / 'kalman_filtered_emg_data.pkl.gz'
            metadata_file = subdir / 'metadata.yaml'
            if emg_data_file.exists() and metadata_file.exists():
                try:
                    # Read and process EMG data
                    emg_data = read_emg_data(emg_data_file)
                    
                    # Read gender from metadata
                    gender = get_gender_from_metadata(metadata_file)
                    
                    # Store data and gender
                    data_store.append((emg_data, gender))
                    if len(emg_data) > max_length:
                        max_length = len(emg_data)
                except Exception as e:
                    print(f"Skipping {emg_data_file} due to error: {e}")
                    continue

    # Pad data to ensure all arrays are of the same length
    for emg_data, label in data_store:
        padded_data = np.pad(emg_data, (0, max_length - len(emg_data)), 'constant')
        all_emg_data.append(padded_data)
        all_labels.append(label)

    X = np.array(all_emg_data)
    y = np.array(all_labels)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize and train the SVM classifier
    svm_clf = SVC(kernel='linear', C=1.0, gamma='scale', random_state=42)
    svm_clf.fit(X_train, y_train)

    # Predict on the test set
    y_pred = svm_clf.predict(X_test)

    # Redirect print output to a string
    output = io.StringIO()

    # Write the classification report with newlines
    output.write("Classification Report for SVM:\n")
    output.write(classification_report(y_test, y_pred))
    output.write("\n")

    # Write cross-validation score with newline
    cv_scores_svm = cross_val_score(svm_clf, X, y, cv=5)
    output.write("CV Average Score for SVM: ")
    output.write(f"{cv_scores_svm.mean()}\n")

    result = output.getvalue()
    output.close()

    print(result)
    return result


def read_emg_data(emg_data_file):
    """Reads and returns the EMG data from a pkl.gz file."""
    with gzip.open(emg_data_file, 'rb') as f:
        emg_data = pickle.load(f)
    return np.array(emg_data).flatten()  # Assuming EMG data is list-like and needs to be flattened

def get_gender_from_metadata(metadata_file):
    """Retrieve the gender from the metadata.yaml file."""
    with metadata_file.open() as f:
        metadata = yaml.safe_load(f)
    gender = metadata.get('subject', {}).get('gender', 'Unknown').lower()
    return 'male' if gender == 'm' else 'female' if gender == 'f' else 'unknown'

if __name__ == '__main__':
    main()
    print("SVM Classifier has been trained and evaluated successfully.")
