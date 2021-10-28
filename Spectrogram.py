#Import Dependencies
import ntpath
import os
import argparse
from numpy import ndarray
import numpy as numpy
from pydub import AudioSegment
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.io import wavfile
from pathlib import Path
from tempfile import mktemp

splitCount=1
summaryDataList = []
summaryNameList = []
summaryFSList = []
numpy.seterr(divide = 'ignore') 

# Validate Inputs
def inputValidate(inDir, outDir, color, xmin, xmax, ymin, ymax):
    if not inDir.exists():
        print("Input file/directory does not exist.")
        exit(1)
    if not outDir.exists():
        print("Output file/directory does not exist.")
        exit(1)
    cmapColors = ['viridis', 'plasma', 'inferno', 'magma', 'cividis',
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn',
            'BrBG','PuOr', 'RdGy', 'RdBu','RdYlBu', 'RdYlGn', 'Spectral',
            'coolwarm', 'bwr', 'seismic']
    if not color in cmapColors:
        print("Color is not available. Colors are case sensitive.")
        exit(1)
    
    if xmin is not None and xmax is not None:
        if xmin > xmax:
            print("Minimum cannot be more than the maximum.")
            exit(1)
    if ymin is not None and ymax is not None:
        if ymin > ymax:
            print("Minimum cannot be more than the maximum.")
            exit(1)

# Read all files
def readDirectory(inDir, outDir, color, xmin, xmax, ymin, ymax, summary):
    # Create ONE figure for Summary
    if summary:
        figureSummary = plt.figure(1, figsize=(50,50), constrained_layout=True)
    # Drill down for audio files
    for root, dirs, files in os.walk(inDir, topdown=True):
        os.chdir(inDir)
        for file in files:
            if file.endswith('.mp3'):
                if summary:
                    createSpectrogram(mp3Handler(root+"\\"+file), file, outDir, color, xmin, xmax, ymin, ymax, summary, figureSummary)
                else:
                    createSpectrogram(mp3Handler(root+"\\"+file), file, outDir, color, xmin, xmax, ymin, ymax, summary)
            elif file.endswith(".wav"):
                if summary:
                    createSpectrogram((root+"\\"+file),file, outDir, color, xmin, xmax, ymin, ymax, summary, figureSummary)
                else:
                    createSpectrogram((root+"\\"+file),file, outDir, color, xmin, xmax, ymin, ymax, summary)
    # Create Spectrogram for Summary
    if summary:
        plotSummary(outDir, color, xmin, xmax, ymin, ymax, figureSummary)

def readFile(inDir, outDir, color, xmin, xmax, ymin, ymax):
    if str(inDir).endswith('.mp3'):
        createSpectrogram(mp3Handler(inDir), ntpath.basename(inDir), outDir, color, xmin, xmax, ymin, ymax)
    else:
        createSpectrogram(inDir,ntpath.basename(inDir), outDir, color, xmin, xmax, ymin, ymax)
                
# MP3 Handler - Creates a temporary wav files for mp3 to create spectrogram
def mp3Handler(file):
    mp3_audio = AudioSegment.from_file(file, format="mp3")  # read mp3
    wname = mktemp('.wav')  # use temporary file
    mp3_audio.export(wname, format="wav")  # convert to wav
    return wname

# Create Spectrogram
def createSpectrogram(file,name,outDir, color, xmin, xmax, ymin, ymax, summary=False, figureSummary=None):
    try:
        FS, data = wavfile.read(file)  # read wav file
    except Exception:
        pass
        print("Error: Skipping ",name, " file unreadable. High probability of being tempered with.")
        return 
    if summary:
        figure = figureSummary
        summaryDataList.append(data[:,1])
        summaryDataList.append(data[:,0])
        summaryNameList.append(str(name))
        summaryFSList.append(FS)
                               
    else:
        global splitCount 
        splitCount+=1
        if data.ndim == 2:
            figure = plt.figure(splitCount, figsize=(100, 10))
            gspec = figure.add_gridspec(ncols=1, nrows=2)
            spec_right = figure.add_subplot(gspec[1])
            spec_left = figure.add_subplot(gspec[0], sharey=spec_right)
            cmap = plt.get_cmap(color) 
            spec_left.specgram(data[:,0], Fs=FS, NFFT=128, noverlap=0, cmap=cmap)  # plot left
            spec_left.set_ylabel("left")
            spec_right.specgram(data[:,1], Fs=FS, NFFT=128, noverlap=0, cmap=cmap)  # plot right
            spec_right.set_ylabel("right")
            
            if xmin is not None :
                spec_left.set_xlim(left=xmin)
                spec_right.set_xlim(left=xmin)
            if xmax is not None :
                spec_left.set_xlim(right=xmax)
                spec_right.set_xlim(right=xmax)
            if ymin is not None:
                spec_left.set_ylim(left=ymin)
                spec_right.set_ylim(left=ymin)
            if ymin is not None:
                spec_left.set_ylim(right=ymax)
                spec_right.set_ylim(right=ymax)
        else:
            figure = plt.figure(splitCount, figsize=(100,10))
            gspec = figure.add_gridspec(ncols=1, nrows=1)
            spec_single = figure.add_subplot()
            cmap = plt.get_cmap(color)
            spec_single.specgram(data, Fs=FS, NFFT=128, noverlap=0, cmap=cmap) # plot single
            spec_single.set_ylabel("One-Dimensional")
            
            if xmin is not None :
                spec_single.set_xlim(left=xmin)
            if xmax is not None :
                spec_single.set_xlim(right=xmax)
            if ymin is not None:
                spec_single.set_ylim(left=ymin)
            if ymin is not None:
                spec_single.set_ylim(right=ymax)
    
        figure.savefig((str(outDir)+'\\'+name+"-Spectrogram.png"))
        
def plotSummary(outDir, color, xmin, xmax, ymin, ymax, figure):
    count = len(summaryNameList)
    gspec = figure.add_gridspec(ncols=1, nrows=((count * 2)))
    cmap = plt.get_cmap(color) 
    for i in range(0,len(summaryDataList),2):
        spec_right = figure.add_subplot(gspec[i])
        spec_right.specgram(summaryDataList[i], Fs=summaryFSList[(i//2)], NFFT=128, noverlap=0, cmap=cmap)  # plot right
        spec_right.set_ylabel("right")
        spec_right.set_title(summaryNameList[(i//2)])
        i+=1
        spec_left = figure.add_subplot(gspec[i])
        spec_left.specgram(summaryDataList[i], Fs=summaryFSList[(i//2)], NFFT=128, noverlap=0, cmap=cmap)  # plot left
        spec_left.set_ylabel("left")
        if xmin is not None :
            spec_left.set_xlim(left=xmin)
            spec_right.set_xlim(left=xmin)
        if xmax is not None :
            spec_left.set_xlim(right=xmax)
            spec_right.set_xlim(right=xmax)
        if ymin is not None:
            spec_left.set_ylim(left=ymin)
            spec_right.set_ylim(left=ymin)
        if ymin is not None:
            spec_left.set_ylim(right=ymax)
            spec_right.set_ylim(right=ymax)
    figure.savefig((str(outDir)+'\\'+"Summary-Spectrogram.png"))
        

#Create Image based on Spectrogram
if __name__ == "__main__":
    
    # Command Line Bash Input, TESTING
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in_path", nargs="?", help="specify input file/directory. If no file is specified, all files within directory and subdirectories are selected", default=Path(os.getcwd()))
    parser.add_argument("out_path",type=Path, help="specify output directory")
    parser.add_argument("-c", "--color",nargs='?', help="default magma, viridis, plasma, inferno, cividis. more at:\nhttps://matplotlib.org/stable/tutorials/colors/colormaps.html", default="magma", const="magma")
    parser.add_argument("-xmn", "--xminimum", help="trim lower x-axis in seconds", type=int, default=None)
    parser.add_argument("-xmx", "--xmaximum", help="trim upper x-axis in seconds", type=int, default=None)
    parser.add_argument("-ymn", "--yminimum", help="trim lower y-axis in Hz", type=int, default=None)
    parser.add_argument("-ymx", "--ymaximum", help="trim upper y-axis in Hz", type=int, default=None)
    parser.add_argument("-s", "--summary", action="store_true", help="summary of all .wav and .mp3 files", default=False)
    
    p = parser.parse_args()
    
    inputValidate(Path(p.in_path), p.out_path, p.color, p.xminimum, p.xmaximum, p.yminimum, p.ymaximum)
    if os.path.isdir(Path(p.in_path)):
        readDirectory(Path(p.in_path), p.out_path, p.color, p.xminimum , p.xmaximum, p.yminimum, p.ymaximum, p.summary)
    else:
        readFile(Path(p.in_path), p.out_path, p.color, p.xminimum , p.xmaximum, p.yminimum, p.ymaximum)