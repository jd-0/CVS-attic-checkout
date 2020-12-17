#!/usr/bin/env python3
# DESCRIPTION #############################
# A basic, badly coded script to checkout files from CVS repos

# USAGE #############################
# Place script within a folder containing the repo folder, and run it.

import re, os, sys

scriptPath = (os.path.dirname(__file__)).replace("\\", "/") # Get file path based on script location

def scanRecurse(baseDir): # Recursively Lists files to process
    for entry in os.scandir(baseDir):
        if entry.is_file(): yield entry.path
        else: yield from scanRecurse(entry.path)
        
def main():
    fileList = scanRecurse(scriptPath) # Find files to process
    for currFile in fileList:
        versionList,currFile = [],currFile.replace("\\", "/") # make path unix-styled
        with open(currFile,'rb') as vFile: currData = vFile.readlines() # open the file as bytes
        if len(currData) == 0 or not currData[0].startswith(b"head\t"): continue # skip files without ',v' encryption

        for pos in range(len(currData)): # get file revision list + dates
            if currData[pos].startswith(b"date\t"): versionList.append((currData[pos-1],currData[pos]))

        print(currFile)
        for revision in versionList:
            currVer = revision[0].replace(b".",b"\.") # conpile a new regex
            pattern = re.compile( currVer + b"log\n@(.*?)@\ntext\n@(.*?)@\n\n\n", re.DOTALL)
            result = re.search(pattern, b"".join(currData) + b"\n\n") # get log info + data for each revision
            if len(result.group(2)) == 0:  continue # skip if no data in that revision

            if result != None: # skip if no regex search results
                newFile = currFile[:len(scriptPath)] + "/co" + currFile[len(scriptPath):]
                newFile = newFile.split('/')
                newFile[-1] = str(revision[0])[2:-3] + "_" + newFile[-1]
                newFile = "/".join(newFile) # made new filename based on rev.no
                if newFile.endswith(",v"): newFile = newFile[:-2] # check for & remove ,v from filename, fix escaped @'s
                newDir = "/".join(newFile.split('/')[:-1]) # make new directory name
                if not os.path.exists(newDir): os.makedirs(newDir) # make new directory if needed
                with open(newFile,'wb') as outFile: outFile.write((result.group(2)).replace(b'@@', b'@')) # write data to file while fixing @'s

                # Log to console
                logVer, logDate = str(revision[0])[2:-3], str(revision[1]).split("\\t")
                print(f"Rev: {logVer}; Date: {logDate[1]} {logDate[2]} \nLog: {str(result.group(1))[2:-3]}\nSize: {len(result.group(2))} bytes\n")
            else: print("No data for", str(revision[0])[2:-3], currFile)
# run program
main()