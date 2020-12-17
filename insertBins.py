#!/usr/bin/env python3
# Usage:
# python insertBins.py rom.bin assetlist.txt

import sys

##to do: padding byte. Low/Hirom

# check args, exit if none specified, read rom & asset list depending on rom name
if len(sys.argv) == 1: print("USAGE: python insertBins.py romfile [assetlist]") ; sys.exit(1)
with open(sys.argv[1],"rb") as currentFile: romData = bytearray(currentFile.read())
if len(sys.argv) == 3: # check if an asset list is specified
    with open(sys.argv[2],"r") as currentFile: assetListing = currentFile.readlines()
else:
    with open(sys.argv[1].replace(".bin", ".txt"),"r") as currentFile: assetListing = currentFile.readlines()

# trim 8000h leading 0's or FF's
if sum(romData[:0x8000]) == 0 or sum(romData[:0x8000]) == 8355840: romData = romData[0x8000:]

romData[0x7fde], romData[0x7fdf] = 0,0 # 7FDE-7FDF Checksum
romSizes = [0x80000,0x100000,0x200000,0x400000] # 4, 8, 16, 32 mbit sizes

for line in assetListing: # parse asset list
    if line[0] == "#" or len(line) < 3: continue # skip comments / short lines
    currAsset = (''.join(c for c in line if c not in '\n\t ')).split(",") # turn line into list

    try: # open current asset
        with open(currAsset[0],"rb") as currentFile: currData = bytearray(currentFile.read())
    except: print("Error opening", currAsset[0]); continue
    
    # get data from current asset, calculate offset
    assetOffset,assetLen,assetBank,assetAddr = int(currAsset[1],16), int(currAsset[3],16), int(currAsset[2][:2],16),int(currAsset[2][2:],16)
    currData = currData[assetOffset:assetOffset+assetLen]
    offset = (assetBank * 0x8000) + (assetAddr - 0x8000)
    offsetEnd = offset + len(currData) 

    if len(romData) < offsetEnd: # extend array so that new data fits
        new_size = offsetEnd - len(romData)
        for i in range(new_size): romData.append(0xFF)

    romData[offset:offsetEnd] = currData # place current asset data in rom
    print(f"{currAsset[0]}:\t\tBank={hex(assetBank)} Addr={hex(assetAddr)} Offset={hex(offset)} Size={hex(assetLen)}")

for i in range(len(romSizes)): # pad data, set rom size in header
    if len(romData) < romSizes[i] and len(romData) not in romSizes: 
        paddAmt = romSizes[i] - len(romData)
        for y in range(paddAmt): romData.append(0xFF); romData[0x7FD7] = i+9

###### write new data to file ######
with open(sys.argv[1].replace(".bin", ".sfc"),'wb') as currentFile: currentFile.write(romData)