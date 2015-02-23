#Problem to solve

These 2 scripts attempt to remove a dependency on the tempo of a song in order to create a reasonable shift between 2 songs.  In previously written software, like the infinite jukebox (infinitejuke.com), the duration of segments is very heavily weighted in determining if a transition should occur.  These scripts remove tempo dependencies by shifting the tempo of a song by a given amount, and by shifting the tempo of one song to match the tempo of another song.

#Inspiration

I am currently taking a CS class named Music Informatics.  We have been studying the Echonest API and looking at software built using this API.  One day in class we got into groups and discussed project ideas.  My group talked about making a project that would continually transition between a group of songs, and the issue of tempo transitions was brought up.  This was where I got the idea to make a script to gradually shift the tempo of a song over a given period of time.

#beatshift.py

Gradually changes the tempo of a song by a given amount starting at a given index over a given peroid of beats.

Usage: python beatshift.py input_filename start_beat shift_length shift_magnitude output_filename

Dependencies: dirac, echonest.remix.audio, pyechonest.track

###Process

Before beatshift.py begins calculating values, the track file is retrieved using pyechonest.track.  This is needed in order to get the tempo of the song.

beatshift.py begins by calculating the linear increment or decrement of the shift.  This is simply the amount to shift divided by the length of the shift.  It then initializes a ratio value to be 1.0.  When shifting the tempo, a ratio of 1.0 means there will be no change in the tempo.  This is necessary to prevent tempo changes before the shift begins.  Lastly, a count variable is initialized to 0.

Using echonest.remix.audio, the audio file is obtaiend using echonest.remix.audio.  This is used to get the array of beats in the song.  In addition, an array named collect is initialized.  This array stores the new beats (changed or not) to make the new song file.

For each beat, the value is stretched by the given ratio.  Until the beginning of the shift is reached, the ratio is 1.0.  While the shift is occuring, the ratio will be changed at each beat to show a gradual change in tempo.  After the shifting is done, the ratio remains at the last calculated value in order to keep the tempo steady for the rest of the song.

#songmix.py

Gradually changes the tempo of a song over a given period of beats to match the tempo of another song.  After the shift the 2nd song will be played starting at a given beat.

Usage: python songmix.py first_filename second_filename start_beat shift_length second_start output_file

Dependencies: dirac, echonest.remix.audio, pyechonest.track

Note: Due to the way pyechonest.track works, the tempo of a song may be interpreted in half time if the tempo is too fast.

###Process

songmix.py works in a very similar manner to beatshift.py, but instead of shifting by a given amount, it will shift a song to match the tempo of another song.  After the shift is done, the beats of the 2nd song will be appended to the list of beats, starting at the given index.
