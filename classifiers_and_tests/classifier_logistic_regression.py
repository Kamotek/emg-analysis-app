import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
import io

def main():
    names = ['Adam', 'Darina', 'Franek', 'Gabi', 'Kajtek', 'Kasia', 'Misia', 'Slawek']
    datasets = ['dataset_1', 'dataset_2', 'dataset_3']
    gender_labels = {'Adam': 'male', 'Darina': 'female', 'Franek': 'male', 'Gabi': 'female', 'Kajtek': 'male', 'Kasia': 'female', 'Misia': 'female', 'Slawek': 'male'}

    all_wavelet_data = []
    all_labels = []

    def read_wavelet_transform_data(folder):
        wavelet_file_path = os.path.join(folder, 'Wavelet Transform.csv')
        wavelet_data = pd.read_csv(wavelet_file_path, header=None, on_bad_lines='skip').values.flatten()
        return wavelet_data

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

    # Create StringIO object to capture print output
    output = io.StringIO()

    # Print the shape of the data
    output.write(f"Shape of X: {X.shape}\n")
    output.write(f"Shape of y: {y.shape}\n")

    # Check class distribution
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

    # Evaluate the classifier
    output.write("Classification Report:\n")
    output.write(f"{classification_report(y_test, y_pred)}\n")

    cv = StratifiedKFold(n_splits=6, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X, y, cv=cv)
    output.write(f"CV Average Score: {cv_scores.mean()}\n")

    # Get the entire string content
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
    print("Logistic regression classifier executed successfully.")
