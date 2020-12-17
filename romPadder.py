#Usage example: 
# python3 romPadder.py "rom.sfc"
# or, just drag 'n' drop!

import sys
romFile = sys.argv[1]
romSizes = [0x80000,0x100000,0x200000,0x400000] # 4, 8, 16, 32 mbit sizes
paddingByte = 0xFF
with open(romFile,'rb') as currentFile: # read data from file
    romData = bytearray(currentFile.read())

for i in range(len(romSizes)): # pad data, set rom size in header
    if len(romData) < romSizes[i] and len(romData) not in romSizes: 
        paddAmt = romSizes[i] - len(romData)
        for y in range(paddAmt): romData.append(paddingByte) ; # romData[0x7FD7] = i+9
        print(f"Padded file {romFile} {hex(paddAmt)} using {paddingByte}'s")

with open(romFile,'wb') as currentFile: #write new data to file
    currentFile.write(romData)
