# python-stuff

Various scripts to do stuff

## bulkCVScheckout

    Gets EVERY revision of every file, including "Attic" folders within CVS repos.

## bytePatch

    Patches a binary file at the specified offset.

## romPadder

    Pads a binary file to lengths of 4, 8, 16, or 32 MBits.

## insertBins

    Inserts files at specified offsets.
      
    Uses a CSV style list in format of [filename],[startPosition],[bank/address],[length].
      
    Example: zl3.CHR,00000,108000,8000

## hex2bin

    Converts Intel hex to binary files, supports 3-byte extended segment addresses
      
    (NOTE: Not my work, I only modified it).
