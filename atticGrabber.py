#!/usr/bin/env python3
# DESCRIPTION #############################
# A basic, badly coded script to restore deleted Attic files from certain CVS repos
# by removing the heading and tailing CVS info from files, and extracting the original data.

# Requirements: Python 3.9 (for logging.basicConfig encoding)

# USAGE #############################
# Place script within a folder containing the repo folder, and run it.

# Grab ONLY v1.2 files:                 python ./atticGrabber.py -v 1.2
# Do a full dry run, with logging:      python ./atticGrabber.py -l True -t True
# Grab ONLY most recent files:          python ./atticGrabber.py -r True

########## TODO ###########
# - Code optimizations?
# - Multiprocessing? Speed improvements?
###########################

# IMPORTS #########################################
import re
import os
import mimetypes
import logging
import argparse
from datetime import datetime

# ARGUMENTS #########################################
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--version", default="None", type=str, help="Specify a single file version number to grab")
ap.add_argument("-l", "--logger", default=True, type=bool, help="Output results to log.txt")
ap.add_argument("-t", "--testrun", default=False, type=bool, help="Do a dry run for testing & logging purposes")
ap.add_argument("-r", "--recent", default=False, type=bool, help="Grab ONLY most recent")
argsCMD = vars(ap.parse_args())

# VARIABLES / INIT #########################################
encodings = ["ISO-8859-1", "UTF-8", "shift-jis"]
extensionsBin = ["bin", "sbin", "bnr", "bpl", "fnt", "gfx", "bnk", "bit", "fnt", "iff", "aifc", "raw", "rel", "swd", "szp", "szs", "sch", "seg", "zzz", "out", "cmd", "app", "res", "narc", "resdat", "cldat", "nsbmd", "ncl", "ncg", "nce", "nsc", "nftr", "pcx", "p3d"]
extensionsText = ['Makedepend', 'Makefile', '.cvsignore', '.s', '.a', '.ev', '.evc', '.i', '.lsf', '.pch', '.imd', '.dfm', '.rsf', '.dtd', '.xlor', '.gmt', '.ose', '.bpr', '.mac', '.gly','.wid', '.nsbtx', '.mk', '.map', '.doc', '.tbl', '.bat', '.dat', '.gmm', '.naix', '.tmp', '.stdout', '.codebook', '.1st', '.lst']
scriptPath = os.path.dirname(__file__) # Get file path based on script location
def scanRecurse(baseDir): # Recursively List files to process
    for entry in os.scandir(baseDir):
        if entry.is_file(): yield entry.path
        else: yield from scanRecurse(entry.path)

print("\n---atticGrabber v2.0---") # Display console info
if argsCMD["logger"] == True: # Logging toggle check
    logname = "{}/log_{}.txt".format(scriptPath, datetime.now().strftime("%d-%m-%y_%H-%M-%S"))
    print("\nCreated logfile at: ", logname)
    logging.basicConfig(filename=logname, filemode='a', level=logging.INFO, encoding=encodings[1])
print("\nSettings:", argsCMD, "\n\nChecking out attics...\n")

# FUNCTIONS #########################################
def setPattern(ver): # set new regex pattern according to version
    verStr = bytes(str(ver), encoding=encodings[1]).replace(b'.', b'\.') # Format the version string
    pattern = re.compile(b'\n' + verStr + b'\nlog\n@(.*?)@\ntext\n@(.*?)@\n\n', re.DOTALL)
    return pattern

def updateLog(*args):
    if argsCMD["logger"] == True: # Clear previous log data
        loggerText = "" # Then, grab all input args, log to file
        for info in args: loggerText += info ; logging.info(loggerText)
        #print(loggerText)
        
def writeFile(currVer, currDate): 
    patternNew = setPattern(currVer) # Set new pattern based on current version
    newData = re.search(patternNew, currData) # extract data with regex
    if newData == None or len(newData.group(2)) == 0: return # No op if empty data
    try: commitMsg = str(newData.group(1), encodings[2]) # Get commit message
    except: commitMsg = "" 
    newData = (newData.group(2)).replace(b'@@', b'@') # Fix for nontext files

    newFile = scriptPath + "/checkout/v" + currVer + "/" + currFile[len(scriptPath)+1:].split("\\", 1)[1] # Make a new filename
    if argsCMD["testrun"] == False: # test/dry run enabled = skip writing files
        os.makedirs(os.path.dirname(newFile), exist_ok=True) # make sure directories exist
        with open(newFile, "wb") as file: file.write(newData) # write bytes to disk

    # Finally, Write results to log
    updateLog("\nWrote file: {}\nSize: {} bytes, Version: {}, Date: {}\nCommit message: {}\n".format(newFile, len(newData), currVer, currDate, commitMsg))

# MAIN PROGRAM #########################################
startTime = datetime.now() ; updateLog("\nStart time: {}\n".format((startTime))) # Get start time
listOfFiles = scanRecurse(scriptPath)

for currFile in listOfFiles: # Iterate thru listed files
        if os.path.dirname(currFile) == scriptPath: continue
        with open(currFile, "rb") as file: # Open file as bytes
            currFileVer = file.readline() # Check if current file has CVS header info
            if currFileVer.startswith(b"head") == False: updateLog("\nSkipping file:" + currFile + "\nNo CVS header found.\n") ; continue
            currData = file.read() # Get file data if CVS info found
        file_name, file_extension = os.path.splitext(currFile) # Get current file extension
        currFileType = str(mimetypes.guess_type(currFile)[0])[:4] # Guess current fileType
        if currFile.endswith('.bat'): currFileType = "text" # Treat .bat as text, not an app
        allVersions = re.findall(b"(.*)\ndate\t(....\...\...)",currData) # List all ver no. / dates in file Data
        verList, dateList = map(list,zip(*allVersions)) # separate tuples, unpacks lists, byte decode, etc.
        verList, dateList = [x.decode() for x in verList], [y.decode() for y in dateList]

        # Write results to log
        updateLog("\nReading file: {}\nAvailable versions: \n{}\n".format(currFile, str(verList)))

        # CHECK CMD LINE ARGS, write data
        if argsCMD["version"] != "None": writeFile(argsCMD["version"], "") # Gets specified version
        elif argsCMD["recent"] == True: writeFile(verList[0], dateList[0]) # Gets "most recent" version
        else: # If nothing specified, default action will be "grab everything"
            for x in range(len(verList)): writeFile(verList[x], dateList[x])

endTime = datetime.now()
updateLog("\nTime taken (seconds): {}\nFinished at: {}\n".format(str(-(startTime - endTime).total_seconds()), endTime))
print("\n...All done!")
