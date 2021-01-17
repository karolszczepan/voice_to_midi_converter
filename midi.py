import numpy as np
from collections import namedtuple

Note = namedtuple('Note', ['value', 'velocity', 'position_in_sec', 'duration'])
RTNote = namedtuple('RTNote', ['value', 'velocity', 'duration'])

def hz_to_midi(frequencies):
    return 12 * (np.log2(np.atleast_1d(frequencies)) - np.log2(440.0)) + 69

