import numpy as np
import itertools
from collections import deque
from app_config import THRESHOLD_WINDOW_SIZE, THRESHOLD_MULTIPLIER, WINDOW_SIZE, SAMPLE_RATE


class OnsetDetector(object):

    def __init__(self):
        self._segments_buf = segments_buf = int(SAMPLE_RATE / WINDOW_SIZE)

        self._thresholding_window_size = THRESHOLD_WINDOW_SIZE
        assert self._thresholding_window_size <= segments_buf

        self._last_spectrum = np.zeros(WINDOW_SIZE, dtype=np.float)
        self._last_flux = deque(
            np.zeros(segments_buf, dtype=np.float), segments_buf)
        self._last_prunned_flux = 0
        # self._last_chunk = np.array()

        self._hanning_window = np.hanning(WINDOW_SIZE)
        # The zeros which will be used to double each segment size
        self._inner_pad = np.zeros(WINDOW_SIZE)

        # To ignore the first peak just after starting the application
        self._first_peak = True
        self._rms_values = []
        self._rms_values_ctr = 0

    def _get_flux_for_thresholding(self):
        # print(list(itertools.islice(
        #     self._last_flux,
        #     self._segments_buf - self._thresholding_window_size,
        #     self._segments_buf)))
        return list(itertools.islice(
            self._last_flux,
            self._segments_buf - THRESHOLD_WINDOW_SIZE,
            self._segments_buf))

    def find_onset(self, samples):
        # windowed = samples*self._hanning_window
        # spectrum = np.abs(np.fft.fft(windowed))
        spectrum = self.autopower_spectrum(samples)
        last_spectrum = self._last_spectrum
        flux = sum(spectrum-last_spectrum)
        thresholded = np.mean(self._get_flux_for_thresholding()) * THRESHOLD_MULTIPLIER
        self._last_flux.append(flux)
        print("thresholded: " + str(thresholded))
        prunned = flux - thresholded if thresholded <= flux else 0
        print("flux: " + str(flux))
        peak = prunned if prunned > self._last_prunned_flux else 0
        self._last_prunned_flux = prunned
        return peak

    def autopower_spectrum(self, samples):
        windowed = samples * self._hanning_window
        # Add 0s to double the length of the data
        padded = np.append(windowed, self._inner_pad)
        # Take the Fourier Transform and scale by the number of samples
        spectrum = np.fft.fft(padded) / WINDOW_SIZE
        autopower = np.abs(spectrum * np.conj(spectrum))
        return autopower[:WINDOW_SIZE]