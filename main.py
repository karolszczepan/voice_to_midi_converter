# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time
import rtmidi
import pyaudio
import wave
import numpy as np
# from pyaudio import PyAudio, paContinue, paInt16


# Press the green button in the gutter to run the script.

def play_midi():
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()

    if available_ports:
        midiout.open_port(1)
    else:
        midiout.open_virtual_port("My virtual output")

    with midiout:
        note_on = [0x90, 65, 112] # channel 1, middle C, velocity 112
        note_off = [0x80, 65, 0]
        midiout.send_message(note_on)
        time.sleep(0.5)
        midiout.send_message(note_off)
    del midiout


def callback(in_data, frame_count, time_info, status):
    data_ok = (in_data, pyaudio.paContinue)
    print(in_data)
    play_midi()
    return data_ok


if __name__ == '__main__':

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)

    print("* recording")

    while stream.is_active():
        time.sleep(0.1)

    # stop stream (6)
    stream.stop_stream()
    stream.close()

    # close PyAudio (7)
    p.terminate()

    print("* done recording")