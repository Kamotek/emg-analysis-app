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
import io

def main():
    # Define the participant names and their corresponding datasets
    names = ['Adam', 'Darina', 'Franek', 'Gabi', 'Kajtek', 'Kasia', 'Misia', 'Slawek']
    datasets = ['dataset_1', 'dataset_2', 'dataset_3']
    gender_labels = {'Adam': 'male', 'Darina': 'female', 'Franek': 'male', 'Gabi': 'female', 
                     'Kajtek': 'male', 'Kasia': 'female', 'Misia': 'female', 'Slawek': 'male'}



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

    max_length = 0
    data_store = []

    for name in names:
        for dataset in datasets:
            data_folder = get_data_folder(name, dataset)
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


    for combined_data, label in data_store:
        padded_data = np.pad(combined_data, (0, max_length - len(combined_data)), 'constant')
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

def get_data_folder(name, dataset):
    base_dir = os.path.dirname(__file__)
    relative_path = os.path.join(
        base_dir,
        '..',
        'preprocessed_data',
        name,
        f'{dataset}',
        'features'
    )
    data_folder = os.path.normpath(relative_path)
    return data_folder

if __name__ == "__main__":
    result = main()
    print(result)
    print("Random Forest classifier executed successfully.")
