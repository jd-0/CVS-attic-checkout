#!/usr/bin/env python3

# Parser for Intel HEX format, intentionally lenient
# This can parse .hex files from the Nintendo leaks, since they use a variant of the format
# with a 3-byte payload in the extended segment address records (most other tools reject this)

# Usage: 
# ./hex2bin.py -i input.hex
# ./hex2bin.py -i input.hex -e big -m 16 -p FF

import binascii, sys, argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, type=str,
	help = "path to input file")
ap.add_argument("-e", "--endian", required=False, type=str, default="big",
	help="endianness of hex data")
ap.add_argument("-m", "--multiply", required=False, type=int, default=8,
	help="offset multiplier")
ap.add_argument("-p", "--padding", required=False, type=str, default="00",
	help="byte to use for padding")
args = vars(ap.parse_args())
paddByte = int(args['padding'],16)

def checksum_of(data): # Sum of byte values
    chk = 0
    for b in data: chk = (chk + b) & 0xff
    # Checksum is two's complement of sum
    return (~chk + 1) & 0xff

def parse_record(lineno, line):
    if not line.startswith(":"): return None

    bs = binascii.unhexlify(line[1:])
    count = bs[0]
    addr = bs[1] << 8 | bs[2]
    rtype = bs[3]
    payload = bs[4:-1]
    checksum = bs[-1]

    if len(payload) != count:
        print("error: invalid payload length on line {} (expected {:02X} bytes, got {:02X})".format(lineno, count, len(payload)), file=sys.stderr)
    
    actual_checksum = checksum_of(bs[:-1])
    if actual_checksum != checksum:
        print("error: invalid checksum on line {} (expected {:02X}, got {:02X})".format(lineno, checksum, actual_checksum), file=sys.stderr)
        sys.exit(1)

    return (rtype, addr, payload)

data = bytearray()
offset = 0

with open(args['input'], "r") as file: fileData = file.readlines()
for (lineno, line) in enumerate(fileData):

    # Skip lines that don't start with a :
    if not line.startswith(":"): continue

    rtype, addr, payload = parse_record(lineno, line.strip())
    if rtype == 0: # Data literal, just write to buffer
        start_addr = offset + addr
        end_addr = offset + addr + len(payload)
        
        # Extend byte array so the data fits
        if len(data) < end_addr:
            new_size = end_addr - len(data)
            for i in range(new_size): data.append(paddByte) # pad with ff or 00

        # Fill array
        data[start_addr:end_addr] = payload
    elif rtype == 1: break # End of file
    elif rtype == 2:
        # Extended segment address, set offset for future data
        # NOTE: File format specifies this must be 2 bytes,
        # but Nintendo seems to use a format with 3 bytes... >.>
        offset = int.from_bytes(payload, byteorder=args['endian'], signed=False) * args['multiply']
    else:
        # We don't support Start Segment Address (03), 
        # Extended Linear Address (04) or Start Linear Address (05)
        # those seem to be x86-specific anyway, so meh
        print("error: unsupported record type {:02X}".format(rtype), file=sys.stderr)
        sys.exit(1)
else: # We ran out of lines before hitting an end of file record (which would break)
    print("error: hit end of input before EOF record", file=sys.stderr)
    sys.exit(1)

# trim 8000h leading 0's or FF's
if sum(data[:0x8000]) == 0 or sum(data[:0x8000]) == 8355840: data = data[0x8000:]

# Print output data to stdout
with open(args['input'].split(".")[0] + '.bin', "wb") as file: file.write(bytes(data))
