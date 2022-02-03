from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
import numpy as np

from fawm22.utils.const import NOTE_FREQS
from fawm22.utils.notes import cos_note

@dataclass
class IntNotationNoteOffset:
    note_idx : int
    octave_offset : int

def _notes_from_int_notation(root_note_idx: int, int_notation: list[int]
                             ) -> list[IntNotationNoteOffset]:
    notes = []
    for offset in int_notation:
        notes.append(IntNotationNoteOffset(
            note_idx = (root_note_idx + offset) % 12,
            octave_offset = (root_note_idx + offset) // 12
        ))
    return notes

def _get_chord_with_int_notation(root_note: str, octave: int,
                                 int_notation: list[int]
                                 ) -> Callable[[np.ndarray],np.ndarray]:
    root_note_idx = list(NOTE_FREQS).index(root_note.upper())
    notes = _notes_from_int_notation(root_note_idx, int_notation)

    note_funcs = []
    for note in notes:
        this_note_str = list(NOTE_FREQS)[note.note_idx]
        this_octave = octave + note.octave_offset
        note_funcs.append(cos_note(this_note_str, this_octave))
    
    return lambda t : sum([func(t) for func in note_funcs])

def major_chord(root_note: str, octave: int
                    ) -> Callable[[np.ndarray],np.ndarray]:
    int_notation = [0,4,7]
    return _get_chord_with_int_notation(root_note, octave, int_notation)

def minor_chord(root_note: str, octave: int
                    ) -> Callable[[np.ndarray],np.ndarray]:
    int_notation = [0,3,7]
    return _get_chord_with_int_notation(root_note, octave, int_notation)