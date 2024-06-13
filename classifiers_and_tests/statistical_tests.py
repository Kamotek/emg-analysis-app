import os
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, f_oneway

def main():
    # Define the paths and individuals
    preprocessed_data_folder = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/preprocessed_data'
    processed_male_data_folder = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/processed_data/male'
    processed_female_data_folder = '/home/kamil/Documents/Projects/emg-data-analysis/emg-data-analysis/processed_data/female'
    male_names = ['Adam', 'Franek', 'Kajtek', 'Slawek']
    female_names = ['Darina', 'Gabi', 'Kasia', 'Misia']
    datasets = ['dataset_1', 'dataset_2', 'dataset_3']

    # Function to read features from CSV files
    def read_features(folder):
        features = {}
        for file_name in os.listdir(folder):
            if file_name.endswith(".csv"):
                feature_name = os.path.splitext(file_name)[0]  # Remove .csv extension
                file_path = os.path.join(folder, file_name)
                # Read CSV file and convert to numeric values
                values = pd.read_csv(file_path, header=None, on_bad_lines='skip').values.flatten()
                numeric_values = pd.to_numeric(values, errors='coerce')
                numeric_values = numeric_values[~np.isnan(numeric_values)]  # Remove NaN values
                features[feature_name] = numeric_values
        return features

    # Dictionary to store features
    male_features = {}
    female_features = {}

    # Read features for each individual and dataset for males
    for name in male_names:
        for dataset in datasets:
            feature_folder = os.path.join(preprocessed_data_folder, name, dataset, 'features')
            if os.path.exists(feature_folder):
                features = read_features(feature_folder)
                for feature_name, values in features.items():
                    if feature_name not in male_features:
                        male_features[feature_name] = []
                    male_features[feature_name].extend(values)

    # Read features for each individual and dataset for females
    for name in female_names:
        for dataset in datasets:
            feature_folder = os.path.join(preprocessed_data_folder, name, dataset, 'features')
            if os.path.exists(feature_folder):
                features = read_features(feature_folder)
                for feature_name, values in features.items():
                    if feature_name not in female_features:
                        female_features[feature_name] = []
                    female_features[feature_name].extend(values)

     # Read additional features for males
    additional_male_features = read_features(processed_male_data_folder)
    for feature_name, values in additional_male_features.items():
         if feature_name not in male_features:
             male_features[feature_name] = []
         male_features[feature_name].extend(values)

     # Read additional features for females
    additional_female_features = read_features(processed_female_data_folder)
    for feature_name, values in additional_female_features.items():
         if feature_name not in female_features:
             female_features[feature_name] = []
         female_features[feature_name].extend(values)

    # Perform t-test and ANOVA for each feature
    t_test_results = {}
    anova_results = {}
    for feature_name in male_features.keys():
        male_values = male_features[feature_name]
        female_values = female_features[feature_name]

        try:
            t_statistic, p_value_ttest = ttest_ind(male_values, female_values)
        except ValueError:
            t_statistic, p_value_ttest = np.nan, np.nan

        try:
            f_statistic, p_value_anova = f_oneway(male_values, female_values)
        except ValueError:
            f_statistic, p_value_anova = np.nan, np.nan

        t_test_results[feature_name] = (t_statistic, p_value_ttest)
        anova_results[feature_name] = (f_statistic, p_value_anova)

    print("T-Test Results:")
    print(t_test_results)
    print("\nANOVA Results:")
    print(anova_results)

if "__name__" == "__main__":
    main()
    print("Done!")