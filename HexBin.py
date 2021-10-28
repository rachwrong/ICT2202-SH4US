import wave
#wr = wave.open("chall3.wav", 'r')
# sample width is 2 bytes
# number of channels is 2
#wave_data = wr.readframes(1)
#wave_data = wr.getframerate()
#wr.close()

import binascii


filename = 'Import\HPinkPanther.wav'
hexTXTFilename = open("hexDump.txt","w")
binTXTFilename = open("binDump.txt","w")

with open(filename, 'rb') as f:
    content = f.read()
    hex = str(binascii.hexlify(content), 'ascii')

    #convert to hex
    formatted_hex = ' '.join(hex[i:i+2] for i in range(0, len(hex), 2))
    hexTXTFilename.writelines(formatted_hex)

    hexTXTFilename.close()

    #convert to bin from hex
    scale = 16 ## equals to hexadecimal
    num_of_bits = 8
    formattedbin = bin(int('1'+hex, 16))[3:]

    #write into test.txt file
    binTXTFilename.writelines(formattedbin)
    binTXTFilename.close()

    f.close()

#################################################
with open("binDump.txt", "r") as binfile:
    stripBinTXTFilename = open("StripBinDump.txt","a")
    #skip to position 45 (352)
    binfile.seek(352)
    for line in binfile:
        extracted = line.strip()[7::8]
        stripBinTXTFilename.writelines(extracted)

    stripBinTXTFilename.close()
    binfile.close()

#with open("StripBinDump.txt", "r") as stripBinfile:
  #  bincontent = stripBinfile.read()
  #  binhex = str(binascii.unhexlify(bincontent))
  #  print(binhex)

  #  stripBinfile.close()