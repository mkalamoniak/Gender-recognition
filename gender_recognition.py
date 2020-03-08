import sys
import os
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import decimate


def recognizer(signal, bitrate, name):
    signal = np.array(signal)
    if len(signal.shape) == 2:
        signal = signal.sum(axis=1) / 2
    n = len(signal)
    signal = signal * np.kaiser(n, 15)
    spectrum = np.abs(fft(signal))

    hps = spectrum.copy()
    duration = n // bitrate
    if duration == 0:
        duration = 1
    for h in np.arange(2, 6):
        dec = decimate(spectrum, h)
        hps[:len(dec)] += dec
    peak_start = 75 * duration

    hps = hps[peak_start:]
    peak = np.argmax(hps)
    frequency = (peak_start + peak) / duration
    gender = 'M' if frequency < 190 else 'K'
    if name[-1] == gender:
        print(frequency, name[-1])
    else:
        hps = hps[:220*duration]
        freqs = range(int(len(hps)))
        freqs = [(peak_start + fq) / duration for fq in freqs]
        plt.title(name + ' ' + str(frequency))
        plt.plot(freqs, hps)
        plt.show()
    return 1 if frequency < 190 else 0



def main():
    path = sys.argv[1]
    name = os.path.splitext(os.path.basename(path))[0]
    raw_data, bitrate = sf.read(path)
    raw_data = np.asarray(raw_data)
    sys.exit(recognizer(raw_data, bitrate, name))


if __name__ == '__main__':
    main()
