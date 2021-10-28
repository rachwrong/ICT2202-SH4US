#Positions   Sample Value         Description
#1 - 4       "RIFF"               Marks the file as a riff file. Characters are each 1. byte long.
#5 - 8       File size (integer)  Size of the overall file - 8 bytes, in bytes (32-bit integer). Typically, you'd fill this in after creation.
#9 -12       "WAVE"               File Type Header. For our purposes, it always equals "WAVE".
#13-16       "fmt "               Format chunk marker. Includes trailing null
#17-20       16                   Length of format data as listed above
#21-22       1                    Type of format (1 is PCM) - 2 byte integer
#23-24       2                    Number of Channels - 2 byte integer
#25-28       44100                Sample Rate - 32 bit integer. Common values are 44100 (CD), 48000 (DAT). Sample Rate = Number of Samples per second, or Hertz.
#29-32       176400               (Sample Rate * BitsPerSample * Channels) / 8.
#33-34       4                    (BitsPerSample * Channels) / 8.1 - 8 bit mono2 - 8 bit stereo/16 bit mono4 - 16 bit stereo
#35-36       16                   Bits per sample
#37-40       "data"               "data" chunk header. Marks the beginning of the data section.
#41-44       File size (data)     Size of the data section, i.e. file size - 44 bytes header.



import struct
import sys

wavFile = sys.argv[1]

if wavFile.endswith('.wav'):
  print("Below is the header information of",wavFile)
  
  #open and read the wav file in binary ('rb')
  fin = open(wavFile,"rb") 
  ChunkID=fin.read(4) #First four bytes are ChunkID which must be "RIFF" in ASCII
  #print(fin.read(4)) #b'\xe8vS\x00'
  if(ChunkID.decode('ASCII') != 'RIFF'):  #check if the first four bytes are RIFF for it to be a WAV file
    print("Not a valid WAV file")
  else:
    print("ChunkID=",ChunkID)
    ChunkSizeString=fin.read(4) # Total Size of File in Bytes - 8 Bytes
    ChunkSize=struct.unpack('I',ChunkSizeString) # 'I' Format is to to treat the 4 bytes as unsigned 32-bit int
    TotalSize=ChunkSize[0]+8 #The subscript is used because struct unpack returns everything as tuple
    print("FileSize=",TotalSize)
    
    DataSize=TotalSize-44 # This is the number of bytes of data
    #print("DataSize=",DataSize)
    
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
    
    with open("Header_Information.txt","w+") as f:
      f.write(wavFile)
      f.write('\n')
      for key, value in Header_Info.items():
         f.write('%s:%s\n' % (key, value))

    fin.close()
  
else:
  print("Not a WAV file, please check your input again!")