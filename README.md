# ICT2202-SH4US

Audio Analysis for mp3 & wav files on Python - Audio Digger
A light weight program that is created to let user do audio analysis easily and quickly.

# User Guide
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

## How to use Audio Digger
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
### How to run Audio Digger
Ensure that current working directory in command prompt is the directory containing AudioDigger.py.

Commands follow this syntax:

python AudioDigger.py [-h]/[-i [in_path]] [-c]/[-xmn]/[-xmx]/[-ymn]/[-ymx] out_path [-bin]/[-hex]/[-head]/[-sp]/[-s]

Examples on how to run commands for different functions:
| Description | Sample Command |
| --- | --- |
| Display and export header information | python AudioDigger.py -i [in_path] [out_path] -head | 
| Create and export spectrograms | python AudioDigger.py -i [in_path] [out_path] -sp |
| Create and export hex dumps | python AudioDigger.py -i [in_path] [out_path] -hex |
| Create and export bin dumps | python AudioDigger.py -i [in_path] [out_path] -bin |

For more information on Audio Digger, please refer to the document Audio Digger User Manual.
