import argparse
import gzip
import pickle
from pathlib import Path

import pandas as pd

GENDER_FILE_NAME = 'gender'
FEATURES_FOLDER_NAME = 'features'

RAW_DATA_FILE = 'emg_raw_data.csv'
FILTERED_DATA_FILE = 'kalman_filtered_emg_data.csv'


def main():
    for subject in args.source_path.iterdir():
        if subject.is_dir():
            for dataset in subject.iterdir():
                if dataset.is_dir():
                    dataset_to_pkl(dataset)

def dataset_to_pkl(dataset_input_path: Path):
    subject_name = dataset_input_path.parent.name
    dataset_output_path = args.output_path / subject_name / dataset_input_path.name
    features_output_path = dataset_output_path / FEATURES_FOLDER_NAME

    features_output_path.mkdir(parents=True, exist_ok=True)

    for file in dataset_input_path.iterdir():
        """
        if file.is_dir():
            if file.name == FEATURES_FOLDER_NAME:
                for feature_file in file.iterdir():
                    input(f'Converting {feature_file.name} to pickle file...')

                    df = pd.read_csv(feature_file)
                    input('Dataframe read. Press Enter to continue...')

                    df.to_pickle(features_output_path / f'{feature_file.stem}.pkl')
        
        else:"""
        if file.name in [RAW_DATA_FILE, FILTERED_DATA_FILE]:
            dataset = file
            df = pd.read_csv(dataset)
            df.attrs.update(parse_subject_metadata(dataset_input_path.parent))

            with gzip.open(dataset_output_path / f'{dataset.stem}.gz', 'wb') as f:
                pickle.dump(df, f)


def parse_subject_metadata(subject_path: Path):
    metadata = {}

    with open(subject_path / GENDER_FILE_NAME) as f:
        gender = f.read()

    metadata.update({'subject_name': subject_path})
    metadata.update({'subject_gender': gender})

    return metadata


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A script to convert experiment structured data to a pickle file.',
        epilog='Example: python structurize_subject_data.py assets/raw assets/processed'
    )

    parser.add_argument(
        'source_path',
        type=Path,
        help='The path to the folder with all subjects and their nested data.'
    )

    parser.add_argument(
        'output_path',
        type=Path,
        help='The path to the output folder for the pickle file.'
    )

    args = parser.parse_args()
    main()
