#Import Dependencies
import binascii
import ntpath
import os
import argparse
import struct
import sys
import numpy as numpy
from pydub import AudioSegment
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.io import wavfile
from pathlib import Path
from tempfile import mktemp

splitCount = 1
summaryDataList = []
summaryDataCount = []
summaryNameList = []
summaryFSList = []
numpy.seterr(divide = 'ignore')

# --------------Dexter & Rachel - Spectrogram--------------
# Validate Inputs for Spectrogram
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

# Read all files for Spectrogram
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
        if data.ndim == 2:
            summaryDataList.append(data[:,1])
            summaryDataList.append(data[:,0])
            summaryDataCount.append(2)
        else:
            summaryDataList.append(data)
            summaryDataCount.append(1)
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
            spec_left.set_title(name)
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
            spec_single.set_title(name)

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
    count = sum(summaryDataCount)
    gspec = figure.add_gridspec(ncols=1, nrows=count)
    cmap = plt.get_cmap(color)
    dataIndex = 0
    fileIndex = 0
    while(dataIndex < len(summaryDataList)):
        if summaryDataCount[fileIndex] == 2:
            spec_right = figure.add_subplot(gspec[dataIndex])
            spec_right.specgram(summaryDataList[dataIndex], Fs=summaryFSList[fileIndex], NFFT=128, noverlap=0, cmap=cmap)  # plot right
            spec_right.set_ylabel("right")
            spec_right.set_title(summaryNameList[(fileIndex)])
            dataIndex +=1
            spec_left = figure.add_subplot(gspec[dataIndex])
            spec_left.specgram(summaryDataList[dataIndex], Fs=summaryFSList[fileIndex], NFFT=128, noverlap=0, cmap=cmap)  # plot left
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
        else:
            spec_single = figure.add_subplot(gspec[dataIndex])
            cmap = plt.get_cmap(color)
            spec_single.specgram(summaryDataList[dataIndex], Fs=summaryFSList[dataIndex], NFFT=128, noverlap=0, cmap=cmap) # plot single
            spec_single.set_ylabel("One-Dimensional")
            spec_single.set_title(summaryNameList[(fileIndex)])
            if xmin is not None :
                spec_single.set_xlim(left=xmin)
            if xmax is not None :
                spec_single.set_xlim(right=xmax)
            if ymin is not None:
                spec_single.set_ylim(left=ymin)
            if ymin is not None:
                spec_single.set_ylim(right=ymax)
        dataIndex += 1
        fileIndex += 1
    figure.savefig((str(outDir)+'\\'+"Summary-Spectrogram.png"))

# --------------KC - Hex Dump--------------
def createHexDump(inDir, outDir, total):
    # Check if user enter -s (they want to export in all audio in the directory)
    if total == True:
        for root, dirs, files in os.walk(inDir, topdown=True):
            os.chdir(inDir)
            for file in files:
                if file.endswith(".mp3") or file.endswith(".wav"):
                    #Open audio file and convert into hex
                    with open(file, 'rb') as audiofile:
                        content = audiofile.read()
                        hex = str(binascii.hexlify(content), 'ascii')
                        #convert to hex
                        formatted_hex = ' '.join(hex[i:i+2] for i in range(0, len(hex), 2))

                        # Write hex content from file into a textfile
                        filepath = os.path.join(outDir, file +'_HexDump.txt')
                        f = open(filepath, "w")
                        f.writelines(formatted_hex)
                        f.close()
                        print("Converted!")
                else:
                    print("Not found!")
    else:
        audioFName = os.path.basename(inDir)
        head, sep, tail = audioFName.partition('.')

        #Open audio file and convert into hex
        with open(inDir, 'rb') as audiofile:
            content = audiofile.read()
            hex = str(binascii.hexlify(content), 'ascii')

            #convert to hex
            formatted_hex = ' '.join(hex[i:i+2] for i in range(0, len(hex), 2))

            # Write hex content from file into a textfile
            filepath = os.path.join(outDir, head + '_HexDump.txt')
            f = open(filepath, "w")
            f.writelines(formatted_hex)
            f.close()

# --------------KC - Bin Dump--------------
def createBinDump(inDir, outDir, total):
    # Check if user enter -s (they want to export in all audio in the directory)
    if total == True:
        for root, dirs, files in os.walk(inDir, topdown=True):
            os.chdir(inDir)
            for file in files:
                if file.endswith(".mp3") or file.endswith(".wav"):
                    #Open audio file and convert into hex
                    with open(file, 'rb') as audiofile:
                        content = audiofile.read()
                        hex = str(binascii.hexlify(content), 'ascii')
                        formatted_hex = ' '.join(hex[i:i+2] for i in range(0, len(hex), 2))
                        #convert to bin from hex
                        scale = 16 ## equals to hexadecimal
                        num_of_bits = 8
                        formattedbin = bin(int('1'+hex, 16))[3:]

                        # Write bin content from file into a textfile
                        filepath = os.path.join(outDir, file + '_BinDump.txt')
                        f = open(filepath, "w")
                        f.writelines(formattedbin)
                        f.close()
                else:
                    print("Not found!")
    else:
        audioName = os.path.basename(inDir)
        head, sep, tail = audioName.partition('.')

        #Open audio file and convert into hex
        with open(inDir, 'rb') as audiofile:
            content = audiofile.read()
            hex = str(binascii.hexlify(content), 'ascii')
            formatted_hex = ' '.join(hex[i:i+2] for i in range(0, len(hex), 2))
            #convert to bin from hex
            scale = 16 ## equals to hexadecimal
            num_of_bits = 8
            formattedbin = bin(int('1'+hex, 16))[3:]

            # Write bin content from file into a textfile
            filepath = os.path.join(outDir, head + '_BinDump.txt')
            f = open(filepath, "w")
            f.writelines(formattedbin)
            f.close()

# --------------Zul & KC - Header Checking--------------
def checkHeader (inPath, outPath, filepath, filename, checksum):
    #open and read the wav file in binary ('rb')
    if(checksum==True):
        fin = open(filepath,"rb")
        ChunkID=fin.read(4) #First four bytes are ChunkID which must be "RIFF" in ASCII

    else:
        fin = open(inPath,"rb")
        ChunkID=fin.read(4) #First four bytes are ChunkID which must be "RIFF" in ASCII

    if(ChunkID.decode('ASCII') != 'RIFF'):  #check if the first four bytes are RIFF for it to be a WAV file
        print("Not a valid WAV file, please try again!")
    else:
        print("ChunkID=",ChunkID)
        ChunkSizeString=fin.read(4) # Total Size of File in Bytes - 8 Bytes
        ChunkSize=struct.unpack('I',ChunkSizeString) # 'I' Format is to to treat the 4 bytes as unsigned 32-bit int
        TotalSize=ChunkSize[0]+8 #The subscript is used because struct unpack returns everything as tuple
        print("FileSize=",TotalSize)

        DataSize=TotalSize-44 # This is the number of bytes of data

        Format=fin.read(4) # "WAVE" in ASCII
        print("Format=",Format)

        SubChunk1ID=fin.read(4) # "fmt " in ASCII
        print("SubChunk1ID=",SubChunk1ID)

        SubChunk1SizeString=fin.read(4) # Should be 16 (PCM, Pulse Code Modulation)
        SubChunk1Size=struct.unpack("I",SubChunk1SizeString) # 'I' format to treat as unsigned 32-bit integer
        print("SubChunk1Size=",SubChunk1Size[0])

        AudioFormatString=fin.read(2) # Should be 1 (PCM)
        AudioFormat=struct.unpack("H",AudioFormatString) # 'H' format to treat as unsigned 16-bit integer
        print("AudioFormat=",AudioFormat[0])

        NumChannelsString=fin.read(2)
        NumChannels=struct.unpack("H",NumChannelsString) # 'H' unsigned 16-bit integer
        print("NumChannels=",NumChannels[0])

        SampleRateString=fin.read(4) #sample rate
        SampleRate=struct.unpack("I",SampleRateString)
        print("SampleRate=",SampleRate[0])

        ByteRateString=fin.read(4)
        ByteRate=struct.unpack("I",ByteRateString) # 'I' unsigned 32 bit integer
        print("ByteRate=",ByteRate[0]) # (Sample Rate* BitsPerSample* Channels) / 8

        BlockAlignString=fin.read(2)
        BlockAlign=struct.unpack("H",BlockAlignString) # 'H' unsigned 16-bit integer
        print("BlockAlign=",BlockAlign[0])

        BitsPerSampleString=fin.read(2) # 16 (CD has 16-bits per sample for each channel)
        BitsPerSample=struct.unpack("H",BitsPerSampleString) # 'H' unsigned 16-bit integer
        print("BitsPerSample=",BitsPerSample[0])

        SubChunk2ID=fin.read(4) # "data" in ASCII
        print("SubChunk2ID=",SubChunk2ID)

        SubChunk2SizeString=fin.read(4) # Number of Data Bytes, Same as DataSize
        SubChunk2Size=struct.unpack("I",SubChunk2SizeString)
        print("SubChunk2Size=",SubChunk2Size[0])

        Header_Info= {'ChunkID': ChunkID.decode('ASCII'), 'FileSize': TotalSize, 'Format': Format, 'SubChunk1ID': SubChunk1ID, 'SubChunk1Size':SubChunk1Size[0],'AudioFormat':AudioFormat[0], 'NumChannels' : NumChannels[0],'SampleRate' : SampleRate[0], 'ByteRate': ByteRate[0], 'BlockAlign' : BlockAlign[0],'BitsPerSample':BitsPerSample[0], 'SubChunk2ID':SubChunk2ID.decode('ASCII'), 'SubChunk2Size' : SubChunk2Size[0]}

        #Write to txt file
        if checksum == True:
            writeToFile = os.path.join(outPath, 'Header_Information_Summary.txt')
            with open(writeToFile, "a+") as af:
                af.write(filepath)
                af.write('\n')
                for key, value in Header_Info.items():
                    af.write('%s:%s\n' % (key, value))
                af.write("--------------------------------- \n")
            fin.close()
        else:
            writeToFile = os.path.join(outPath, filename + '_Header_Information.txt')
            with open(writeToFile, "w+") as f:
                f.write(filepath)
                f.write('\n')
                for key, value in Header_Info.items():
                    f.write('%s:%s\n' % (key, value))
            fin.close()

# --------------Zul - Header Information--------------
def headerInformation (inDir, outDir, allHeaders):
    # Check if user enter -s (they want to export in all audio in the directory)
    if allHeaders == True:
        print("Checked!")
        for root, dirs, files in os.walk(inDir, topdown=True):
            os.chdir(inDir)
            for file in files:
                if file.endswith(".wav"):
                    headAll, sepAll, tailAll = file.partition('.')
                    checkHeader(inDir, outDir, file, headAll, allHeaders)
                    print(headAll)
                else:
                    print("Not found!")
    else:
        audioName = os.path.basename(inDir)
        head, sep, tail = audioName.partition('.')

        #Check if file is wav
        if tail.endswith('wav'):
            print("Below is the header information of", audioName)

            # call checking header method
            checkHeader(inDir, outDir, audioName, head, allHeaders)
        else:
            print("Not a WAV file, please check your input again!")

#Main Method
if __name__ == "__main__":

    # Command Line Bash Input
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in_path", nargs="?", help="specify input file/directory. If no file is specified, all files within directory and subdirectories are selected", default=Path(os.getcwd()))
    parser.add_argument("out_path",type=Path, help="specify output directory")

    # --------------Dexter & Rachel--------------
    parser.add_argument("-sp", "--spectrogram", help="Create a spectrogram of the audio file", action="store_true", default=None)
    parser.add_argument("-c", "--color",nargs='?', help="default magma, viridis, plasma, inferno, cividis. more at:\nhttps://matplotlib.org/stable/tutorials/colors/colormaps.html", default="magma", const="magma")
    parser.add_argument("-xmn", "--xminimum", help="trim lower x-axis in seconds", type=int, default=None)
    parser.add_argument("-xmx", "--xmaximum", help="trim upper x-axis in seconds", type=int, default=None)
    parser.add_argument("-ymn", "--yminimum", help="trim lower y-axis in Hz", type=int, default=None)
    parser.add_argument("-ymx", "--ymaximum", help="trim upper y-axis in Hz", type=int, default=None)
    parser.add_argument("-s", "--summary", action="store_true", help="summary of all .wav and .mp3 files", default=False)

    # --------------KC--------------
    parser.add_argument("-bin", "--binary", help="Create a binary dump of the audio file", action="store_true", default=None)
    parser.add_argument("-hex", "--hexadecimal", help="Create a hexadecimal dump of the audio file", action="store_true", default=None)

    # --------------Zul--------------
    parser.add_argument("-head", "--header", help="Extract out the Header information of the audio file", action="store_true", default=None)

    p = parser.parse_args()

    inputValidate(Path(p.in_path), p.out_path, p.color, p.xminimum, p.xmaximum, p.yminimum, p.ymaximum)

    # if hex
    if p.hexadecimal:
        createHexDump(Path(p.in_path), p.out_path, p.summary)

    # if bin
    elif p.binary:
        createBinDump(Path(p.in_path), p.out_path, p.summary)

    # if header
    elif p.header:
        headerInformation(Path(p.in_path), p.out_path, p.summary)

    # if spectragram directory
    elif p.spectrogram and os.path.isdir(Path(p.in_path)):
        readDirectory(Path(p.in_path), p.out_path, p.color, p.xminimum , p.xmaximum, p.yminimum, p.ymaximum, p.summary)

    # if spectragram file
    elif p.spectrogram:
        readFile(Path(p.in_path), p.out_path, p.color, p.xminimum, p.xmaximum, p.yminimum, p.ymaximum)

    else:
        print("Wrong syntax, please try again!")
