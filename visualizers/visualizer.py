from matplotlib import pyplot as plt

from backend.emg_signal import EMGSignal


class Visualizer:
    def __init__(self, signal: EMGSignal):
        self._signal = signal

    @property
    def plot(self) -> plt.Figure:
        flattened_signal = self._signal.signal.values.flatten()  # Possibly not most performant

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(flattened_signal, label='EMG Signal')
        ax.set_title('EMG Signal')
        ax.set_xlabel('Sample Number')
        ax.set_ylabel('Amplitude')
        ax.legend()

        return fig


if __name__ == '__main__':
    channels = 128
    sample_rate = 500

    data = [i + 0.1 for i in range(channels)]
    signal = EMGSignal(channels, sample_rate)

    for _ in range(10):
        signal.add_data_row(data)

    visualizer = Visualizer(signal)
    visualizer.plot.show()
