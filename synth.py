import rtmidi
from midi import RTNote
import threading


class Synth(object):

    def __init__(self):
        self._midiout = rtmidi.MidiOut()
        self._available_ports = self._midiout.get_ports()
        self._current_note = RTNote(60, 100, 50)
        self.e = threading.Event()
        self._finish = False

    def set_new_note(self, note):
        self._current_note = note
        print("Freq " + str(self._current_note.value))

    def run(self):
        print("inside synth loop")
        self.e.wait()
        self.e.clear()

        while not self._finish:
            if self._available_ports:
                self._midiout.open_port(1)
            else:
                self._midiout.open_virtual_port("My virtual output")
            with self._midiout:
                note_on = [0x90, self._current_note.value, self._current_note.velocity]
                note_off = [0x80, self._current_note.value, 0]
                self._midiout.send_message(note_on)
                print("Waiting...")
                try:
                    self.e.wait(timeout=8)
                except SystemError:
                    print("TIMEOUT OCCURED! EXIT...")
                    self._finish = True;
                self.e.clear()
                print("Waiting done")
                self._midiout.send_message(note_off)

    def close_midi_port(self):
        del self._midiout
