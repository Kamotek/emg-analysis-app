    # TODO implement signal-to-noise ratio (SNR) feature extractor
    # similar to this one

    # Define the noise segment (for simplicity, using the first 100 samples as noise)
    noise_segment = emg_flattened_signal[:100]
    signal_segment = emg_flattened_signal

    # Function to calculate SNR
    def calculate_snr(signal, noise):
        signal_power = np.mean(signal**2)
        noise_power = np.mean(noise**2)
        snr = 10 * np.log10(signal_power / noise_power)
        return snr

    # Calculate SNR
    snr = calculate_snr(signal_segment, noise_segment)
    print(f'SNR: {snr:.2f} dB')