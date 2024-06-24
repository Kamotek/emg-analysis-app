import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
import yaml
import gzip
import pickle
from pathlib import Path
import io

def main():
    base_dir = Path("assets/band")  # Set base directory for searching data
    all_emg_data = []
    all_labels = []

    max_length = 0
    data_store = []

    # Function to read EMG data from a pkl.gz file
    def read_emg_data(emg_data_file):
        with gzip.open(emg_data_file, 'rb') as f:
            emg_data = pickle.load(f)
        return np.array(emg_data).flatten()  # Flatten to a 1D array

    # Function to get gender from metadata.yaml file
    def get_gender_from_metadata(metadata_file):
        with metadata_file.open() as f:
            metadata = yaml.safe_load(f)
        gender = metadata.get('subject', {}).get('gender', 'unknown').lower()
        return 'male' if gender == 'm' else 'female' if gender == 'f' else 'unknown'

    # Search for files in the directory
    for subdir in base_dir.rglob('*'):
        if subdir.is_dir():
            emg_data_file = subdir / 'kalman_filtered_emg_data.pkl.gz'
            metadata_file = subdir / 'metadata.yaml'
            if emg_data_file.exists() and metadata_file.exists():
                try:
                    emg_data = read_emg_data(emg_data_file)
                    gender = get_gender_from_metadata(metadata_file)
                    if gender != 'unknown':
                        data_store.append((emg_data, gender))
                        if len(emg_data) > max_length:
                            max_length = len(emg_data)
                except Exception as e:
                    print(f"Skipping {emg_data_file} due to error: {e}")
                    continue

    # Pad data to ensure consistent length
    for emg_data, label in data_store:
        padded_data = np.pad(emg_data, (0, max_length - len(emg_data)), 'constant')
        all_emg_data.append(padded_data)
        all_labels.append(label)

    X = np.array(all_emg_data)
    y = np.array(all_labels)

    output = io.StringIO()
    output.write(f"Shape of X: {X.shape}\n")
    output.write(f"Shape of y: {y.shape}\n\n")

    class_distribution = pd.Series(y).value_counts()
    output.write(f"Class distribution:\n{class_distribution}\n\n")

    max_components = min(X.shape[0], X.shape[1], 16)

    pipeline = make_pipeline(
        StandardScaler(),
        PCA(n_components=max_components),
        LogisticRegression(random_state=42)
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    output.write("Classification Report:\n")
    output.write(f"{classification_report(y_test, y_pred)}\n")

    cv = StratifiedKFold(n_splits=6, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X, y, cv=cv)
    output.write(f"CV Average Score: {cv_scores.mean()}\n")

    result = output.getvalue()
    output.close()

    print(result)
    return result

if __name__ == "__main__":
    result = main()
    print(result)
    print("Logistic regression classifier executed successfully.")
