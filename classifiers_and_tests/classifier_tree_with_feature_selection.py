import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.feature_selection import SelectKBest, f_classif
from imblearn.over_sampling import SMOTE
import yaml
import gzip
import pickle
import io
from pathlib import Path

def main():
    base_dir = Path("assets/band")

    all_wavelet_data = []
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
        all_wavelet_data.append(padded_data)
        all_labels.append(label)

    X = np.array(all_wavelet_data)
    y = np.array(all_labels)

    output = io.StringIO()

    # Print the shape of the data
    output.write(f"Shape of X: {X.shape}\n")
    output.write(f"Shape of y: {y.shape}\n\n")

    # Check class distribution
    class_distribution = pd.Series(y).value_counts()
    output.write(f"Class distribution:\n{class_distribution}\n\n")

    # Apply SMOTE for balancing classes
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Apply feature selection
    selector = SelectKBest(f_classif, k=50)
    X_resampled_selected = selector.fit_transform(X_resampled, y_resampled)

    pipeline = make_pipeline(
        StandardScaler(),
        RandomForestClassifier(random_state=42)
    )

    X_train, X_test, y_train, y_test = train_test_split(X_resampled_selected, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled)

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    # Evaluate the classifier
    output.write("Classification Report:\n")
    output.write(f"{classification_report(y_test, y_pred)}\n\n")

    # Cross-validation score
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X_resampled_selected, y_resampled, cv=cv)
    output.write(f"CV Average Score: {cv_scores.mean()}\n")

    result = output.getvalue()
    output.close()

    return result

def read_emg_data(emg_data_file):
    """Reads and returns the EMG data from a pkl.gz file."""
    with gzip.open(emg_data_file, 'rb') as f:
        emg_data = pickle.load(f)
    return np.array(emg_data).flatten()  # Assuming EMG data is list-like and needs to be flattened

def get_gender_from_metadata(metadata_file):
    """Retrieve the gender from the Metadata.yaml file."""
    with metadata_file.open() as f:
        metadata = yaml.safe_load(f)
    gender = metadata.get('subject', {}).get('gender', 'Unknown').lower()
    return 'male' if gender == 'm' else 'female' if gender == 'f' else 'unknown'

if __name__ == "__main__":
    result = main()
    print(result)
    print("Random Forest classifier executed successfully.")
