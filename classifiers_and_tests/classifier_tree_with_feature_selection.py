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

def main():
    # Define the paths for processed data
    processed_male_data_folder = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/processed_data/male'
    processed_female_data_folder = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/processed_data/female'
    # Define the participant names and their corresponding datasets
    names = ['Adam', 'Darina', 'Franek', 'Gabi', 'Kajtek', 'Kasia', 'Misia', 'Slawek']
    datasets = ['dataset_1', 'dataset_2', 'dataset_3']
    # Mapping of names to gender
    gender_labels = {'Adam': 'male', 'Darina': 'female', 'Franek': 'male', 'Gabi': 'female', 
                     'Kajtek': 'male', 'Kasia': 'female', 'Misia': 'female', 'Slawek': 'male'}

    # Initialize lists to store wavelet transform data and labels
    all_wavelet_data = []
    all_labels = []

    # Function to read wavelet transform data from a given path
    def read_wavelet_transform_data(folder):
        wavelet_file_path = os.path.join(folder, 'Wavelet Transform.csv')
        wavelet_data = pd.read_csv(wavelet_file_path, header=None, on_bad_lines='skip').values.flatten()
        return wavelet_data

    # Function to read wavelet transform frequency data from a given path
    def read_wavelet_transform_freq_data(folder):
        wavelet_freq_file_path = os.path.join(folder, 'Wavelet Transform_frequencies.csv')
        wavelet_freq_data = pd.read_csv(wavelet_freq_file_path, header=None, on_bad_lines='skip').values.flatten()
        return wavelet_freq_data

    # Read data for individual participants and their datasets
    max_length = 0
    data_store = []

    for name in names:
        for dataset in datasets:
            data_folder = f'/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/preprocessed_data/{name}/{dataset}/features'
            try:
                wavelet_data = read_wavelet_transform_data(data_folder)
                wavelet_freq_data = read_wavelet_transform_freq_data(data_folder)
                combined_data = np.concatenate((wavelet_data, wavelet_freq_data))
                data_store.append((combined_data, gender_labels[name]))
                if len(combined_data) > max_length:
                    max_length = len(combined_data)
            except Exception as e:
                print(f"Skipping {name}-{dataset} due to error: {e}")
                continue

    # Read data from male and female directories
    for gender, data_folder in [('male', processed_male_data_folder), ('female', processed_female_data_folder)]:
        for name in os.listdir(data_folder):
            name_folder = os.path.join(data_folder, name)
            if os.path.isdir(name_folder):
                for dataset in os.listdir(name_folder):
                    dataset_folder = os.path.join(name_folder, dataset)
                    if os.path.isdir(dataset_folder):
                        try:
                            wavelet_data = read_wavelet_transform_data(dataset_folder)
                            wavelet_freq_data = read_wavelet_transform_freq_data(dataset_folder)
                            combined_data = np.concatenate((wavelet_data, wavelet_freq_data))
                            data_store.append((combined_data, gender))
                            if len(combined_data) > max_length:
                                max_length = len(combined_data)
                        except Exception as e:
                            print(f"Skipping {name}-{dataset} due to error: {e}")
                            continue

    # Pad data to ensure all records have the same length
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

    # Apply SMOTE for balancing classes
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Apply feature selection
    selector = SelectKBest(f_classif, k=50)  # Selecting top 50 features
    X_resampled_selected = selector.fit_transform(X_resampled, y_resampled)

    # Create a pipeline with StandardScaler and RandomForestClassifier
    pipeline = make_pipeline(
        StandardScaler(),
        RandomForestClassifier(random_state=42)
    )

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_resampled_selected, y_resampled, test_size=0.8, random_state=42, stratify=y_resampled)

    # Train the random forest model
    pipeline.fit(X_train, y_train)

    # Predict on the test set
    y_pred = pipeline.predict(X_test)

    # Evaluate the classifier
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Cross-validation score
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X_resampled_selected, y_resampled, cv=cv)
    print("CV Average Score:", cv_scores.mean())

if __name__ == "__main__":
    main()
    print("Random Forest classifier executed successfully.")
