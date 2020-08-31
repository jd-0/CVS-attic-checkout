# Description: 
# Copies all folders + files specified in attics.txt 
# while preserving folder hierarchy.

# Usage: 
# Make a list of directories to copy in "attics.txt",
# For example: find . -iname "attic*" > attics.txt
# Place "atticExtract.py" and "attics.txt" in a directory 
# containing the repo, and run the script.

import shutil

# Edit the source and destination as necessary
source = "bbgames.cvs"
destination = "bbgames-attic"

with open("attics.txt", "r") as attics:
    for line in attics:
        line = line.rstrip()
        dst = line.replace(source,destination) 
        shutil.copytree(line, dst) 
