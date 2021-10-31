# ICT2202-SH4US

Audio Analysis on Python - Audio Digger

Feature 1 - Showing and exporting the header of the audio files (wav and mp3)

Wav File Format
- Export Header information of a single audio out as a txt file [DONE]
- Export Header information of audios from a folder out as a txt file (summary of all headers) [DONE]

MP3 File Format
- Export Header information of a single audio out as a txt file [WIP]
- Export Header information of audios from a folder out as a txt file (summary of all headers) [NOT DONE]

Feature 2 - Showing and exporting of Spectrogram analysis of audio files (wav and mp3)

Wav & MP3 File Format
- Export Spectrogram analysis of a single audio file [DONE]
- Export Spectrogram analysis of audio files from a folder (summary of all headers) [DONE]

Feature 3 - Exporting of Hex Dump & Bin Dump of Audio file

Hex Dump
- Export Hex dump of a single audio out as a txt file [DONE]
- Export Hex dump of audios from a folder out as separate txt files (summary of all hexes) [DONE]

Bin Dump
- Export Bin dump of a single audio out as a txt file [DONE]
- Export Bin dump of audios from a folder out as separate txt files (summary of all binaries) [DONE]

# User Guide
## Audio Digger (WIP)
A command-line based audio analysis tool that is able to read .wav and .mp3 files.

## Prerequisites
This program requires python(at least 3.8) to be installed on your machine as well as these python packages: 
1. matplotlib
2. pydub
3. scipy

You can either install this by downloading requirements.txt and running pip install -r requirements.txt or installing them manually with the following commands:

1. pip install matplotlib
2. pip install pydub
3. pip install scipy 

The program also requires having ffmpeg installed. You can download ffmpeg using the following link: 
https://www.ffmpeg.org/download.html

Ensure that ffmpeg is installed into the correct directories and is a system environment variable, you can refer to
https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10

## How to use Audio Digger (WIP)
### Functions
Audio Digger has the following functions:
1. Display header information of the audio files, header information will also be exported into a .txt file
2. Create spectrograms and exports them as .png files
3. Export hex dumps of the audio files into a .txt file
4. Export bin dump of the audio files into a .txt file
### Commands
The following are arguments that can be used when running Audio Digger:
| Argument | Full Argument | Description |
| --- | --- | --- |
| -h | --help | Shows help message and exits |
| -i | --in_path | Specify input file/directory. If no files is specified, all files in the specified directory are selected |
| -sp | --spectrogram | Create a spectrogram of the audio file |
| -c | --color | default magma, viridis, plasma, inferno, cividis. more at: https://matplotlib.org/stable/tutorials/colors/colormaps.html |
| -xmn | --xminimum | trim lower x-axis in seconds |
| -xmx | --xmaximum | trim upper x-axis in seconds |
| -ymn | --yminimum | trim lower y-axis in seconds |
| -ymx | --ymaximum | trim upper y-axis in seconds |
| -s | --summary | summary of all .wav and .mp3 files |
| -bin | --binary | Create a binary dump of the audio file |
| -hex | --hexadecimal | Create a hexadecimal dump of the audio file |
| -head | --header | Extract out the Header information of the audio file |
