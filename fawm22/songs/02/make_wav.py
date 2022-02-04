import os
from typing import Callable

import numpy as np
from scipy.io.wavfile import write
from fawm22.utils.chords import major_chord, minor_chord
from fawm22.utils.square import square_wave

SAMPLE_RATE = 44100
BEATS_PER_MIN = 70
NUM_SUB_BEATS = 4

def _num_samples(num_beats:float) -> int:
    seconds_per_beat = 60/BEATS_PER_MIN
    samples_per_beat = int(round(seconds_per_beat * SAMPLE_RATE))
    return int(round(samples_per_beat * num_beats))

def beat_edge_fader(num_beats:float=1.0, threshhold:float=0.8):
    x = np.linspace(0,1,_num_samples(num_beats))
    fader = 1 - 1/(1+np.exp(-150*(x-threshhold)))
    fader = fader*fader[::-1]
    return fader

def time(num_beats:float=1.0) -> np.ndarray:
    return np.arange(_num_samples(num_beats))/SAMPLE_RATE

def silence() -> Callable[[],np.ndarray]:
    return lambda t: np.zeros_like(t)

def main():
    track1 = []
    for _ in range(84+64):
        track1.append(square_wave('c',2)(time(1/3))*beat_edge_fader(1/3))
        track1.append(square_wave('g',2)(time(1/3))*beat_edge_fader(1/3))
        track1.append(square_wave('e',2)(time(1/3))*beat_edge_fader(1/3))

    track2 = []
    for _ in range(4):
        track2.append(silence()(time(1)))

    track2.append(square_wave('c',4)(time(1)))
    track2.append(square_wave('b',3)(time(1)))
    track2.append(square_wave('c',4)(time(1/8)))
    track2.append(square_wave('a',3)(time(15/8)))

    track2.append(square_wave('c',4)(time(1)))
    track2.append(square_wave('b',3)(time(1)))
    track2.append(square_wave('c',4)(time(1/8)))
    track2.append(square_wave('e',4)(time(15/8)))

    track2.append(square_wave('c',4)(time(1)))
    track2.append(square_wave('b',3)(time(1)))
    track2.append(square_wave('c',4)(time(1/8)))
    track2.append(square_wave('a',3)(time(15/8)))

    track2.append(square_wave('c',4)(time(1)))
    track2.append(square_wave('b',3)(time(1)))
    track2.append(square_wave('c',4)(time(1/8)))
    track2.append(square_wave('e',4)(time(15/8)))

    for _ in range(128):
        track2.append(silence()(time(1)))
        
    data1 = np.concatenate(track1)
    data2 = np.concatenate(track2)

    output_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(output_path,'data','song.wav')
    write(output_path, SAMPLE_RATE, data1+data2)

if __name__ == "__main__":
    main()