
import io
import os
import numpy as np
import pandas as pd
from sklearn.svm import SVC
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

    # Function to read wavelet transform data and frequencies from a given path
    def read_wavelet_transform_data(folder, label):
        wavelet_file_path = os.path.join(folder, 'Wavelet Transform.csv')
        frequencies_file_path = os.path.join(folder, 'Wavelet Transform_frequencies.csv')
        wavelet_data = pd.read_csv(wavelet_file_path, header=None, on_bad_lines='skip').values.flatten()
        frequencies_data = pd.read_csv(frequencies_file_path, header=None, on_bad_lines='skip').values.flatten()
        combined_data = np.concatenate((wavelet_data, frequencies_data), axis=0)  # Combine wavelet and frequencies data

            
        additional_data_files = ['Mean Absolute Value.csv', 'Mean Frequency.csv', 'Median Frequency.csv', 'Root Mean Square.csv']
        for file_name in additional_data_files:
            file_path = os.path.join(folder, file_name)
            additional_data = pd.read_csv(file_path, header=None, on_bad_lines='skip').values.flatten()
            combined_data = np.concatenate((combined_data, additional_data), axis=0)
            
        return combined_data, label

    # Read data for individual names and datasets
    for name in names:
        for dataset in datasets:
            data_folder = get_data_folder(name, dataset)
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

    return result


def get_data_folder(name, dataset):
    # Get the current script's directory
    base_dir = os.path.dirname(__file__)
    
    # Construct the relative path
    relative_path = os.path.join(
        base_dir,
        '..',  # Move up one directory
        'preprocessed_data',
        name,
        f'{dataset}',
        'features'  # Adjust the dataset part as requested
    )

    # Normalize the path to remove any redundant separators
    data_folder = os.path.normpath(relative_path)
    
    return data_folder



if __name__ == '__main__':
    main()
    print("SVM Classifier has been trained and evaluated successfully.")