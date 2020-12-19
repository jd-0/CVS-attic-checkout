# Usage:
# python bytePatch.py rom.sfc 7fc0 "LA LEGENDE DE ZELDA   "
# python bytePatch.py rom.sfc 7fd9 6

import sys

if len(sys.argv) == 1: print("USAGE: python bytePatch.py romfile (string/int)") ; sys.exit(1)
# open input file as byte array, get input offset
with open(sys.argv[1],'rb') as f: buff = bytearray(f.read())
offset = int(sys.argv[2], 16)

if sys.argv[3].isdecimal(): # check if input is string
    byteValue = int(sys.argv[3], 16)
    buff[offset] = byteValue
    print("Patched byte at offset",hex(offset))

else: # convert str to hex, write offset

    byteValue = [] # convert string to list of hex, then write to buffer
    for n in sys.argv[3]: byteValue.append(ord(n))
    for i in range(len(byteValue)): buff[offset+i] = byteValue[i]
    print("Patched byte(s) at offset",hex(offset))
# write data
with open(sys.argv[1],'wb') as f: f.write(buff)
