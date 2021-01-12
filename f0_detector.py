import numpy as np

from app_config import FREQUENCY_RANGE, SAMPLE_RATE

class F0Detector(object):

    def __init__(self):
        self._min_freq, self._max_freq = FREQUENCY_RANGE

    def find_f0(self, samples):
        cepstrum = self.calculate_cepstrum(samples)
        start = int(SAMPLE_RATE / self._max_freq)
        end = int(SAMPLE_RATE / self._min_freq)
        narrowed_cepstrum = cepstrum[start:end]

        peak_ix = narrowed_cepstrum.argmax()
        freq0 = SAMPLE_RATE / (start + peak_ix)

        if freq0 < self._min_freq or freq0 > self._max_freq or np.isnan(freq0):
            print("Detected frequency is out of bounds: " + str(freq0))
            return
        return freq0

    # def autopower_spectrum(self, samples):
    #     """
    #     Calculates a power spectrum of the given data using the Hamming window.
    #     """
    #     # TODO: check the length of given samples; treat differently if not
    #     # equal to the window size
    #
    #     windowed = samples * self._hanning_window
    #     # Add 0s to double the length of the data
    #     padded = np.append(windowed, self._inner_pad)
    #     # Take the Fourier Transform and scale by the number of samples
    #     spectrum = np.fft.fft(padded) / self._window_size
    #     autopower = np.abs(spectrum * np.conj(spectrum))
    #     return autopower[:self._window_size]

    def calculate_cepstrum(self, samples):
        spectrum = np.fft.fft(samples)
        log_spectrum = np.log(np.abs(spectrum))
        return np.fft.ifft(log_spectrum).real