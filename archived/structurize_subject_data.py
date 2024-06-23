import argparse
import gzip
import pickle
from pathlib import Path

import pandas as pd
import yaml

from backend.data_manager import DataManager

GENDER_FILE_NAME = 'gender'
FEATURES_FOLDER_NAME = 'features'

RAW_DATA_FILE = 'emg_raw_data.csv'
FILTERED_DATA_FILE = 'kalman_filtered_emg_data.csv'


def main():
    data_manager = DataManager()
    data_manager.BAND_ASSETS_PATH.mkdir(parents=True, exist_ok=True)

    for subject in ARGS.source_path.iterdir():
        if subject.is_dir():
            for dataset_folder in subject.iterdir():
                if dataset_folder.is_dir():
                    new_dataset_path = ARGS.output_path / data_manager._next_dataset_name()
                    new_dataset_path.mkdir(parents=True, exist_ok=True)

                    dataset_to_pkl(dataset_folder, new_dataset_path)
                    metadata_to_yaml(subject, new_dataset_path)


def dataset_to_pkl(folder_input_path: Path, dataset_output_path: Path):
    for file in folder_input_path.iterdir():
        if file.name in [RAW_DATA_FILE, FILTERED_DATA_FILE]:
            dataset = file
            data = pd.read_csv(dataset)

            with gzip.open(dataset_output_path / f'{dataset.stem}.pkl.gz', 'wb') as f:
                pickle.dump(data, f)


def metadata_to_yaml(dataset_input_path: Path, metadata_output_path: Path):
    metadata = {'subject': parse_subject_metadata(dataset_input_path)}

    with open(metadata_output_path / f'metadata.yaml', 'w') as f:
        yaml.dump(metadata, f)


def parse_subject_metadata(subject_path: Path):
    metadata = {}

    with open(subject_path / GENDER_FILE_NAME) as f:
        gender = f.read()

    metadata.update({'name': subject_path.name})
    metadata.update({'gender': gender})

    return metadata


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A script to convert experiment structured data to a pickle file.',
        epilog='Example: python structurize_subject_data.py assets/raw assets/band'
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

    ARGS = parser.parse_args()
    main()
