import numpy as np

from fawm22.utils.notes import cos_note
from fawm22.utils.const import NOTE_FREQS

def square_wave(note, octave):
    freq = (2**octave)*NOTE_FREQS[note.upper()]
    n = np.arange(100)[::2] + 1
    # return lambda t: (0.1) * np.sum(np.sin(n[np.newaxis]*2*np.pi*freq*t[:,np.newaxis])/n[np.newaxis],axis=1)
    return lambda t: 0.01*np.sign(np.sin(2*np.pi*freq*t))