import time
import numpy as np
from pyaudio import PyAudio, paContinue
from midi import hz_to_midi, RTNote
from synth import Synth
from f0_detector import F0Detector
from onset_detector import OnsetDetector
from app_config import WINDOW_SIZE
import wave

from matplotlib import pyplot as plt
import librosa

# rms = np.sqrt(np.mean(data**2))
# self._rms_values.append(rms)
# self._rms_values_ctr += 1
# if self._rms_values_ctr == 100:
#     plt.figure()
#     plt.plot(self._rms_values)
#     plt.show()
#     self._rms_values.clear()
#     self._rms_values_ctr = 0
# print(np.sqrt(np.mean(data**2)))


class Voice2Midi(object):

    def __init__(self):
        self._synth = Synth()
        self._onset_detector = OnsetDetector()
        self._f0_detector = F0Detector()
        self._wf = wave.open('vocal2.wav', 'rb')
        self._p = PyAudio()
        self._stream = self._p.open(format=self._p.get_format_from_width(self._wf.getsampwidth()),
                        channels=self._wf.getnchannels(),
                        rate=self._wf.getframerate(),
                        output=True,
                        frames_per_buffer=WINDOW_SIZE,
                        stream_callback=self._process_frame)

    def run(self):

        # self._stream = pya.open(
        #     format=paInt16,
        #     channels=1,
        #     rate=SAMPLE_RATE,
        #     input=True,
        #     frames_per_buffer=WINDOW_SIZE,
        #     stream_callback=self._process_frame,
        # )
        # self._stream.start_stream()

        # self._stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),


        print(self._wf.getframerate())
        self._stream.start_stream()

        while self._stream.is_active() and not input():
            time.sleep(0.1)

        self._stream.stop_stream()
        self._stream.close()
        self._p.terminate()

    def _process_frame(self, in_data, frame_count, time_info, status_flag):
        data = self._wf.readframes(frame_count)
        # print(data)
        data_array = np.frombuffer(data, dtype=np.int32)
        # print(np.shape(data))
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
                note = RTNote(midi_note_value, 100, 0.05)
                self._synth.play_note(note)
        return data, paContinue


if __name__ == '__main__':
    proc = Voice2Midi()
    proc.run()
