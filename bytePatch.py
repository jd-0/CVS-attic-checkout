# Usage:
# python bytePatch.py rom.sfc 7fc0 "LA LEGENDE DE ZELDA   "
# python bytePatch.py rom.sfc 0x7fd9 0xaa
# python bytePatch.py rom.sfc 7fde 0 0

import sys

if len(sys.argv) == 1: print("USAGE: python bytePatch.py romfile (string/int)") ; sys.exit(1)

with open(sys.argv[1],'rb') as f: buff = bytearray(f.read())
offset = int(sys.argv[2], 16)

if len(sys.argv) > 4: # Try to parse input as a list of hex
    print(sys.argv[3:])
    inputBytes = sys.argv[3:]
    for i in range(len(inputBytes)): buff[offset+i] = int(inputBytes[i], 16)
    #print('1')

elif sys.argv[3].startswith('0x'): # if only one byte input, must specify it is hex
    inputBytes = int(sys.argv[3], 16)
    buff[offset] = inputBytes
    #print('2')

else: # otherwise, treat input as string
    inputBytes = []
    for n in sys.argv[3]: inputBytes.append(ord(n)) # conv str to list of hex
    for i in range(len(inputBytes)): buff[offset+i] = inputBytes[i]
    #print('3')

print(f"Patched {inputBytes}, at offset {hex(offset)}")
# write data
with open(sys.argv[1],'wb') as f: f.write(buff)
