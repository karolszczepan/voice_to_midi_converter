import time
import numpy as np
from pyaudio import PyAudio, paContinue
from midi import hz_to_midi, RTNote
from synth import Synth
from f0_detector import F0Detector
from onset_detector import OnsetDetector
from app_config import WINDOW_SIZE
import threading
import wave

from matplotlib import pyplot as plt
import librosa

class Voice2Midi(object):

    def __init__(self):
        self._synth = Synth()
        self._onset_detector = OnsetDetector()
        self._f0_detector = F0Detector()
        self._wf = wave.open('vocal2.wav', 'rb')
        self._p = PyAudio()
        self._e = threading.Event()
        self._stream = self._p.open(format=self._p.get_format_from_width(self._wf.getsampwidth()),
                        channels=self._wf.getnchannels(),
                        rate=self._wf.getframerate(),
                        output=True,
                        frames_per_buffer=WINDOW_SIZE,
                        stream_callback=self._process_frame)

    def run(self):
        print(self._wf.getframerate())
        self._stream.start_stream()
        # while self._stream.is_active() and not input():

        self._synth.run()

        self._stream.stop_stream()
        self._stream.close()
        self._p.terminate()

    def _process_frame(self, in_data, frame_count, time_info, status_flag):
        data = self._wf.readframes(frame_count)
        data_array = np.frombuffer(data, dtype=np.int32)
        if np.shape(data_array)[0] == WINDOW_SIZE and np.shape(np.nonzero(data_array))[1] > 0:
            # print(np.shape(np.nonzero(data_array))[1])
            data_array = data_array.astype('float32')
            data_array = data_array / np.max(data_array)

            # onset = self._onset_detector.find_onset(data_array)
            if self._onset_detector.find_onset(data_array):
                freq0 = self._f0_detector.find_f0(data_array)
                if freq0:
                    # Onset detected
                    print("Note detected; fundamental frequency: ", freq0)
                    midi_note_value = int(hz_to_midi(freq0)[0])
                    print("Midi note value: ", midi_note_value)
                    note = RTNote(midi_note_value, 100, 0.5)
                    self._synth.set_new_note(note)
                    self._synth.e.set()
            return data, paContinue
        else:
            return


if __name__ == '__main__':
    proc = Voice2Midi()
    proc.run()

