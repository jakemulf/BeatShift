"""
songmix.py

Takes 2 songs and shifts the tempo of the first one over a given peroid of time to match the tempo of the 2nd one.

After the shift is done, the second song will be played starting at a given index.

Created by Jacob Mulford on 2/19/2015

Based on https://github.com/echonest/remix/blob/master/examples/stretch/simple_stretch.py
"""
import dirac
from echonest.remix import audio
from pyechonest import track

usage = """
Usage: python songmix.py <first_filename> <second_filename> <start_beat> <shift_length> <second_start> <output_file>

Example: python songmix.py CallMeMaybe.mp3 YouCanCallMeAl.mp3 10 50 25 YouCanCallMeMaybe.mp3

This will shift the tempo of CallMeMaybe.mp3 to match the tempo of YouCanCallMeAl.mp3.  This shift will begin at beat 10
of CallMeMaybe.mp3, will last 50 beats, and will transition into beat 25 of YouCanCallMeAl.mp3.  The output file will me
YouCanCallMeMaybe.mp3
"""

def main(first_filename, second_filename, start_beat, shift_length, second_start, output_filename):
    t1 = track.track_from_filename(first_filename)
    t2 = track.track_from_filename(second_filename)

    beat_difference = t2.tempo - t1.tempo

    beat_increment = beat_difference/shift_length
    beat_ratio = 1.0
    beat_count = 0

    audiofile1 = audio.LocalAudioFile(first_filename)
    beats1 = audiofile1.analysis.segments
    collect = []

    while (beat_count < start_beat + shift_length and beat_count < len(beats1)):
        if (beat_count > start_beat and beat_count <= shift_length + start_beat):
            desired_bmp = beat_increment * (beat_count - start_beat) + t1.tempo
            beat_ratio = t1.tempo/desired_bmp

        beat_audio = beats1[beat_count].render()
        scaled_beat = dirac.timeScale(beat_audio.data, beat_ratio)
        ts = audio.AudioData(ndarray=scaled_beat, shape=scaled_beat.shape,
                sampleRate=audiofile1.sampleRate, numChannels=scaled_beat.shape[1])
        collect.append(ts)

        beat_count = beat_count + 1

    beat_count = second_start

    audiofile2 = audio.LocalAudioFile(second_filename)
    beats2 = audiofile2.analysis.segments

    while (beat_count < len(beats2)):
        beat_audio = beats2[beat_count].render()
        scaled_beat = dirac.timeScale(beat_audio.data, 1.0)
        ts = audio.AudioData(ndarray=scaled_beat, shape=scaled_beat.shape,
                sampleRate=audiofile2.sampleRate, numChannels=scaled_beat.shape[1])
        collect.append(ts)
 
        beat_count = beat_count + 1

    out = audio.assemble(collect, numChannels=2)
    out.encode(output_filename)

if __name__ == '__main__':
    import sys
    try:
        first_filename = sys.argv[1]
        second_filename = sys.argv[2]
        start_beat = int(sys.argv[3])
        shift_length = int(sys.argv[4])
        second_start = int(sys.argv[5])
        output_filename = sys.argv[6]
    except:
        print usage
        sys.exit(-1)
    main(first_filename, second_filename, start_beat, shift_length, second_start, output_filename)
