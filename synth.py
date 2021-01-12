import time
import rtmidi


class Synth(object):

    def __init__(self):
        self._midiout = rtmidi.MidiOut()
        self._available_ports = self._midiout.get_ports()

        # if self._available_ports:
        #     self._midiout.open_port(1)
        # else:
        #     self._midiout.open_virtual_port("My virtual output")


    def play_note(self, note):
        if self._available_ports:
            self._midiout.open_port(1)
        else:
            self._midiout.open_virtual_port("My virtual output")

        with self._midiout:
            note_on = [0x90, note.value, note.velocity]
            note_off = [0x80, note.value, 0]
            self._midiout.send_message(note_on)
            time.sleep(note.duration)
            self._midiout.send_message(note_off)

    def close_midi_port(self):
        del self._midiout
