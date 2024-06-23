import asyncio

import pandas as pd

from backend.feature_extractor import FeatureExtractor
from backend.filter import Filter


class EMGSignal:
    """
    A wrapper around a pandas DataFrame that represents an EMG signal.
    It also provides a way to stream the signal data (not fully implemented).

    In the future, it could be extended to provide more advanced signal processing methods
    (filters, feature extraction, etc.).

    The signal is a time series of EMG data, where each row represents a moment in time
    and each column represents the signal value for a specific channel.
    """
    def __init__(self, channels, sample_rate):
        self.channels = channels
        self.sample_rate = sample_rate

        self._signal = pd.DataFrame(columns=range(channels))
        self._signal_queue = asyncio.Queue()

        self._filters_scheduled_queue = []
        self._features_scheduled = []

        self._filters_applied = []
        self._features_extracted = {}

    def add_data_row(self, channels_values: list):
        self._signal_queue.put_nowait(channels_values)

    def _is_signal_outdated(self) -> bool:
        return not self._signal_queue.empty()

    @property
    def signal(self) -> pd.DataFrame:
        if self._is_signal_outdated:
            self._sync_signal()
        return self._signal

    def _sync_signal(self):
        signal_latest_rows = []
        while not self._signal_queue.empty():
            signal_latest_rows.append(self._signal_queue.get_nowait())
        self._signal = pd.concat([self._signal, pd.DataFrame(signal_latest_rows)])

    async def stream(self):
        # TODO: streaming should be done with asyncio, nice framework for dealing with IO-bound tasks
        # https://docs.python.org/3/library/asyncio.html
        # https://realpython.com/async-io-python/
        # note: threading could also be used, but it has more complex API
        # note: multiprocessing could also be used, but it has a lot more complex API; it's more for CPU-bound tasks
        while True:
            yield await self._signal_queue.get()

    def schedule_filter(self, emg_filter: Filter):
        self._filters_scheduled_queue.append(emg_filter)

    def apply_filters(self):
        assert self._filters_scheduled_queue, "No filters scheduled"
        assert self._is_signal_outdated(), "Signal dataframe is not up-to-date"

        while self._filters_scheduled_queue:
            emg_filter = self._filters_scheduled_queue.pop(0)
            self._signal = emg_filter.filter(self._signal)
            self._filters_applied.append(emg_filter)

    def schedule_feature_extraction(self, feature_extractor: FeatureExtractor):
        self._features_scheduled.append(feature_extractor)

    def extract_features(self):
        assert self._is_signal_outdated(), "Signal dataframe is not up-to-date"

        for feature_extractor in self._features_scheduled:
            feature_dataframe = feature_extractor.extract(self._signal)
            self._features_extracted[feature_extractor] = feature_dataframe


async def main():
    channels = 128
    sample_rate = 500

    data = [i + 0.1 for i in range(channels)]
    signal = EMGSignal(channels, sample_rate)

    for _ in range(10):
        signal.add_data_row(data)

    print(signal.signal)
    # note - here I don't really test the asyncio cause I don't even know how yet

if __name__ == '__main__':
    asyncio.run(main())
