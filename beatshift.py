"""
beatshift.py

Shifts the beat of a file over a given period of time by a given magnitude at the given interval

Created by Jacob Mulford on 2/18/2015

Based on https://github.com/echonest/remix/blob/master/examples/stretch/simple_stretch.py
"""
import math
import os
import sys
import dirac
from echonest.remix import audio
from pyechonest import track

usage = """
Usage: python beatshift.py <input_filename> <start_beat> <shift_length> <shift_magnitude> <output_filename>

Example: python beatshift.py CallMeMaybe.mp3 10 50 -10 CallMeShift.mp3

This will shift the tempo of CallMeMaybe.mp3 by -10 bpm over 50 beats starting at beat 10.

This program will not run if the magnitude of the shift is +/- 8% of the default beat.
"""

def main(input_filename, start_beat, shift_length, shift_magnitude, output_filename):
    t = track.track_from_filename(input_filename)
    difference = abs(shift_magnitude)
    average = (t.tempo + (shift_magnitude * 0.5))

#    if (difference*1.0/average > 0.08):
 #       print "Error: magnitude of the shift is greater than +/- 8% of the default beat."
  #      sys.exit(-1)

    beat_ratio_base = (1.0*shift_magnitude/shift_length)/t.tempo
    beat_ratio = 1.0
    beat_count = 0

    audiofile = audio.LocalAudioFile(input_filename)
    beats = audiofile.analysis.beats
    collect = []

    print t.tempo

    for beat in beats:
        if (beat_count > start_beat and beat_count <= shift_length + start_beat):
            desired_bpm = ((1.0*beat_count - start_beat)/(shift_length))*shift_magnitude + t.tempo
            print desired_bpm
            beat_ratio = t.tempo/desired_bpm


        beat_audio = beat.render()
        scaled_beat = dirac.timeScale(beat_audio.data, beat_ratio)
        ts = audio.AudioData(ndarray=scaled_beat, shape=scaled_beat.shape,
                sampleRate=audiofile.sampleRate, numChannels=scaled_beat.shape[1])
        collect.append(ts)

        beat_count = beat_count + 1

    out = audio.assemble(collect, numChannels=2)
    out.encode(output_filename)

if __name__ == '__main__':
    import sys
    try:
        input_filename = sys.argv[1]
        start_beat = int(sys.argv[2])
        shift_length = int(sys.argv[3])
        shift_magnitude = float(sys.argv[4])
        output_filename = sys.argv[5]
    except:
        print usage
        sys.exit(-1)
    main(input_filename, start_beat, shift_length, shift_magnitude, output_filename)
