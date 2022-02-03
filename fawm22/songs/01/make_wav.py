import os
from typing import Callable

import numpy as np
from scipy.io.wavfile import write
from fawm22.utils.chords import major_chord, minor_chord

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
    track = []
    track.append(major_chord('c',3)(time(3/4))*beat_edge_fader(3/4))
    track.append(minor_chord('e',3)(time(3/4))*beat_edge_fader(3/4))
    track.append(minor_chord('d',3)(time(3/4))*beat_edge_fader(3/4))
    track.append(minor_chord('d',3)(time(3/4))*beat_edge_fader(3/4))
    track.append(minor_chord('d',3)(time(3/4))*beat_edge_fader(3/4))
    track.append(silence()(time(1/4)))

    main
    data = np.concatenate(track*4)
    quarter = data.shape[0]//4
    data = np.tile(data, 2)

    data[2*quarter:8*quarter] += 0.4*major_chord('c',4)(time(24))*beat_edge_fader(24, 0.98)
    data[3*quarter:8*quarter] += 0.2*major_chord('c',5)(time(20))*beat_edge_fader(20, 0.97)
    
    data *= 0.1

    output_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(output_path,'data','song.wav')
    write(output_path, SAMPLE_RATE, data)

if __name__ == "__main__":
    main()