#!/usr/bin/env python3
# Usage:
# ./insertBins.py -i rom.bin
# ./insertBins.py -i rom.bin -a assetlist.txt -p FF

import argparse

##to do:  Low vs Hirom

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, type=str,
	help = "path to input file")
ap.add_argument("-a", "--assets", required=False, type=str,
	help="path to assets list with file names, offsets, etc")
ap.add_argument("-p", "--padding", required=False, type=str, default="00",
	help="byte to use for padding")
args = vars(ap.parse_args())
paddByte = int(args['padding'],16)

if args['assets'] == None: # read rom & asset list depending on rom name
    with open((args['input'].split("."))[0] + '.txt',"r") as currentFile: assetListing = currentFile.readlines()
else:
    with open(args['assets'],"r") as currentFile: assetListing = currentFile.readlines()
with open(args['input'],"rb") as currentFile: romData = bytearray(currentFile.read())

# trim 8000h leading 0's or FF's
# if sum(romData[:0x8000]) == 0 or sum(romData[:0x8000]) == 8355840: romData = romData[0x8000:]

romSizes = [0x80000,0x100000,0x200000,0x400000] # 4, 8, 16, 32 mbit sizes

for line in assetListing: # parse asset list
    if line[0] == "#" or len(line) < 5: continue # skip comments / short lines
    currAsset = (''.join(c for c in line if c not in '\n\t ')).split(",") # turn line into list

    try: # open current asset
        with open(currAsset[0],"rb") as currentFile: currData = bytearray(currentFile.read())
    except: print("Error opening", currAsset[0]); continue
    
    # get data from current asset, calculate offset
    assetOffset,assetLen,assetBank,assetAddr = int(currAsset[1],16), int(currAsset[3],16), int(currAsset[2][:-4],16),int(currAsset[2][-4:],16)
    currData = currData[assetOffset:assetOffset+assetLen]
    offset = (assetBank * 0x8000) + (assetAddr - 0x8000)
    offsetEnd = offset + len(currData) 

    if len(romData) < offsetEnd: # extend array so that new data fits
        new_size = offsetEnd - len(romData)
        for i in range(new_size): romData.append(paddByte)

    romData[offset:offsetEnd] = currData # place current asset data in rom
    print(f"{currAsset[0]}:\t\tBank={hex(assetBank)} Addr={hex(assetAddr)} Offset={hex(offset)} Size={hex(assetLen)}")

for i in range(len(romSizes)): # pad data, set rom size in header
    if len(romData) < romSizes[i] and len(romData) not in romSizes: 
        paddAmt = romSizes[i] - len(romData)
        for y in range(paddAmt): romData.append(paddByte) #; romData[0x7FD7] = i+9

###### write new data to file ######
with open(args['input'].split(".")[0] + '.sfc','wb') as currentFile: currentFile.write(romData)