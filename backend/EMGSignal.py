import asyncio

import pandas as pd


class EMGSignal:
    def __init__(self, channels, sample_rate):
        self.channels = channels
        self.sample_rate = sample_rate

        self._signal = pd.DataFrame(columns=range(channels))
        self._signal_queue = asyncio.Queue()

    def add_data_row(self, channels_values: list):
        self._signal_queue.put_nowait(channels_values)

    def _is_signal_outdated(self):
        return not self._signal_queue.empty()

    @property
    def signal(self):
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
