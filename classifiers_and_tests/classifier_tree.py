import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report
import io

def main():
    # Names and datasets
    names = ['Adam', 'Darina', 'Franek', 'Gabi', 'Kajtek', 'Kasia', 'Misia', 'Slawek']
    datasets = ['dataset_1', 'dataset_2', 'dataset_3']
    gender_labels = {'Adam': 'male', 'Darina': 'female', 'Franek': 'male', 'Gabi': 'female',
                     'Kajtek': 'male', 'Kasia': 'female', 'Misia': 'female', 'Slawek': 'male'}

    all_wavelet_data = []
    all_labels = []

    def read_wavelet_transform_data(folder, label):
        wavelet_file_path = os.path.join(folder, 'Wavelet Transform.csv')
        frequencies_file_path = os.path.join(folder, 'Wavelet Transform_frequencies.csv')
        wavelet_data = pd.read_csv(wavelet_file_path, header=None, on_bad_lines='skip').values.flatten()
        frequencies_data = pd.read_csv(frequencies_file_path, header=None, on_bad_lines='skip').values.flatten()
        combined_data = np.concatenate((wavelet_data, frequencies_data), axis=0)  # Combine data
        return combined_data, label

    base_dir = os.path.dirname(__file__)  # Get base directory for relative paths

    for name in names:
        for dataset in datasets:
            data_folder = os.path.join(base_dir, f'../preprocessed_data/{name}/{dataset}/features')
            try:
                combined_data, label = read_wavelet_transform_data(data_folder, gender_labels[name])
                all_wavelet_data.append(combined_data)
                all_labels.append(label)
            except Exception as e:
                print(f"Skipping {name}-{dataset} due to error: {e}")
                continue

    max_length = max(len(data) for data in all_wavelet_data)
    padded_combined_data = [np.pad(data, (0, max_length - len(data)), 'constant') for data in all_wavelet_data]

    X = np.array(padded_combined_data)
    y = np.array(all_labels)

    output = io.StringIO()
    output.write(f"Shape of X: {X.shape}\n")
    output.write(f"Shape of y: {y.shape}\n\n")

    class_distribution = pd.Series(y).value_counts()
    output.write(f"Class distribution:\n{class_distribution}\n\n")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    rf_clf = RandomForestClassifier(n_estimators=110, random_state=42)
    rf_clf.fit(X_train, y_train)

    y_pred = rf_clf.predict(X_test)

    output.write("Classification Report:\n")
    output.write(f"{classification_report(y_test, y_pred)}\n\n")

    cv_scores = cross_val_score(rf_clf, X, y, cv=5)
    output.write(f"CV Average Score: {cv_scores.mean()}\n")

    result = output.getvalue()
    output.close()

    return result

if __name__ == "__main__":
    result = main()
    print(result)
    print("Classifier Tree completed.")
