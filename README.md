#beatshift.py

Gradually changes the tempo of a song by a given amount starting at a given index over a given peroid of beats.

Usage: python beatshift.py <input_filename> <start_beat> <shift_length> <shift_magnitude> <output_filename>

Dependencies: dirac, echonest.remix.audio, pyechonest.track

###Process

Before beatshift.py begins calculating values, the track file is retrieved using pyechonest.track.  This is needed in order to get the tempo of the song.

beatshift.py begins by calculating the linear increment or decrement of the shift.  This is simply the amount to shift divided by the length of the shift.  It then initializes a ratio value to be 1.0.  When shifting the tempo, a ratio of 1.0 means there will be no change in the tempo.  This is necessary to prevent tempo changes before the shift begins.  Lastly, a count variable is initialized to 0.

Using echonest.remix.audio, the audio file is obtaiend using echonest.remix.audio.  This is used to get the array of beats in the song.  In addition, an array named collect is initialized.  This array stores the new beats (changed or not) to make the new song file.

For each beat, the value is stretched by the given ratio.  Until the beginning of the shift is reached, the ratio is 1.0.  While the shift is occuring, the ratio will be changed at each beat to show a gradual change in tempo.  After the shifting is done, the ratio remains at the last calculated value in order to keep the tempo steady for the rest of the song.
