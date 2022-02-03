from __future__ import annotations
from typing import Callable

import numpy as np

from fawm22.utils.const import NOTE_FREQS

def cos_note(note: str, octave: int, phase: float=0
             )-> Callable[[np.ndarray],np.ndarray]:
    note = note.upper()
    freq = NOTE_FREQS[note] * (2**octave)
    return lambda t : np.cos(2*np.pi*freq*t + phase)