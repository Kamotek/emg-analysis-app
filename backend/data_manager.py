import gzip
import pickle
from pathlib import Path

import pandas as pd
import yaml

from backend.emg_signal import EMGSignal


class DataManager:
    """
    A class that manages the storage and retrieval of EMG data and metadata.

    It uses pickle and gzip for data serialization and compression, and yaml for metadata serialization.
    This way, the data can be stored in a compact and efficient way.
    """
    DATA_DEFAULT_NAME = 'emg_raw_data'
    METADATA_DEFAULT_NAME = 'metadata'

    def __init__(self):
        self.PROJECT_PATH = Path(__file__).parent.parent
        assert self.PROJECT_PATH.name == 'emg-analysis-app', 'Project path is not as expected'

        self.ASSETS_PATH = self.PROJECT_PATH / 'assets'
        self.BAND_ASSETS_PATH = self.ASSETS_PATH / 'band'

        self.DATA_FORMAT = '.pkl.gz'
        self.METADATA_FORMAT = '.yaml'

        self.BAND_ASSETS_PATH.mkdir(parents=True, exist_ok=True)

    def list_datasets(self):
        return [d.name for d in self.BAND_ASSETS_PATH.iterdir() if d.is_dir()]

    def _DATASET_FOLDER(self, dataset_id: str) -> Path:
        return self.BAND_ASSETS_PATH / dataset_id

    def load_dataset(self, dataset_id: str) -> EMGSignal:
        data = self.load_data(dataset_id)
        metadata = self.load_metadata(dataset_id)
        return EMGSignal(data, metadata)

    def load_data(self, dataset_id: str, file_name: str = DATA_DEFAULT_NAME) -> pd.DataFrame:
        dataset_folder = self._DATASET_FOLDER(dataset_id)
        if not dataset_folder.exists():
            raise ValueError(f'Dataset {dataset_id} does not exist')

        else:
            with gzip.open(dataset_folder / (file_name + self.DATA_FORMAT), 'rb') as f:
                return pickle.load(f)

    def load_metadata(self, dataset_id: str) -> dict:
        metadata_path = self._DATASET_FOLDER(dataset_id) / f'{self.METADATA_DEFAULT_NAME}{self.METADATA_FORMAT}'
        if not metadata_path.exists():
            raise ValueError(f'Metadata for dataset {dataset_id} does not exist')
        else:
            with open(metadata_path, 'r') as f:
                return yaml.safe_load(f)

    def store_dataset_from_signal(self, signal: EMGSignal, data_name: str = DATA_DEFAULT_NAME, metadata_name: str = METADATA_DEFAULT_NAME):
        self.store_dataset(signal.signal, signal.metadata, data_name, metadata_name)

    def store_dataset(self, data: pd.DataFrame, metadata: dict, data_name: str = DATA_DEFAULT_NAME, metadata_name: str = METADATA_DEFAULT_NAME):
        dataset_folder = self._create_new_dataset_folder()

        self._store_data(data, dataset_folder, data_name)
        self._store_metadata(metadata, dataset_folder, metadata_name)

    def _store_data(self, data: pd.DataFrame, dataset_folder: Path, file_name: str):
        with gzip.open(dataset_folder / f'{file_name}{self.DATA_FORMAT}', 'wb') as f:
            pickle.dump(data, f)

    def _store_metadata(self, metadata: dict, dataset_folder: Path, file_name: str):
        with open(dataset_folder / f'{file_name}{self.METADATA_FORMAT}', 'w') as f:
            yaml.dump(metadata, f)

    def _create_new_dataset_folder(self):
        new_dataset_name = self._next_dataset_name()
        new_dataset_path = self._DATASET_FOLDER(new_dataset_name)
        new_dataset_path.mkdir()
        return new_dataset_path

    def _next_dataset_name(self):
        datasets = [d for d in self.BAND_ASSETS_PATH.iterdir() if d.is_dir() and d.name.isdigit()]

        if not datasets:
            new_folder = '1'
        else:
            last_folder = max(datasets, key=lambda d: int(d.name))
            last_number = int(last_folder.name)
            new_folder = f'{last_number + 1}'
        return new_folder


if __name__ == '__main__':
    data_manager = DataManager()
    print(data_manager.load_dataset('24'))
    next_dataset = data_manager._next_dataset_name()
    data_manager.store_dataset_from_signal(data_manager.load_dataset('24'))
    print(data_manager.load_dataset(next_dataset))

    print(data_manager.list_datasets())

    for dataset_id in data_manager.list_datasets():
        metadata = data_manager.load_metadata(dataset_id)
        print(f'Dataset {dataset_id}: {metadata}')
