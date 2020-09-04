##########################################
# Description:
# A basic, badly coded script to restore deleted Attic files from certain CVS repos
# by removing the heading and tailing CVS info from files, and extracting the original data.

# Requirements: Python 3.9

# Usage:
# Place script in folder containing the repo, and run it.
# Grab every version of every file:     ./atticGrabber.py -a True
#                                       ./atticGrabber.py --all True
# Grab ONLY v1.2 files:                 ./atticGrabber.py -v 1.2
# Do a full dry run, with logging:      ./atticGrabber.py -l True -t True -a True
# Grab ONLY most recent files:          ./atticGrabber.py -r True

# Todo: 
# DeDupe / detect files when grabbing all? 
# Cleanup!!

# IMPORTS #########################################
import re
import os
import mimetypes
import logging
import argparse

# ARGUMENTS #########################################
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--version", default="1.1",
                help="Specify a single file version number to grab")
ap.add_argument("-a", "--allfiles", default=False, type=bool,
                help="Grab all possible file versions")
ap.add_argument("-l", "--logger", default=False, type=bool,
                help="Output results to log.txt")
ap.add_argument("-t", "--testrun", default=False, type=bool,
                help="Do a dry run for testing & logging purposes")
ap.add_argument("-r", "--recent", default=False, type=bool,
                help="Grab ONLY most recent")
args = vars(ap.parse_args())
#verNo = int((str(args["version"]).split("."))[1])
print("---atticGrabber v1.0---\n\nChecking out attics...\n")
print("Settings:", args)

# VARS #########################################
encodings = ["ISO-8859-1","UTF-8"]
extensionsBin = ["bin", "sbin", "bnr", "bpl", "fnt", "gfx", "bnk", "bit", "fnt", "iff", "aifc", "raw", "rel", "swd", "szp", "szs", "sch", "seg", "zzz", "out", "cmd", "app", "res", "narc", "resdat", "cldat", "nsbmd", "ncl", "ncg", "nce", "nsc", "nftr", "pcx", "p3d"]
extensionsText = ['Makedepend', 'Makefile', '.cvsignore', '.s', '.a', '.ev', '.evc', '.i', '.lsf', '.pch', '.imd', '.dfm', '.rsf', '.dtd', '.xlor', '.gmt', '.ose', '.bpr', '.mac', '.gly','.wid', '.nsbtx', '.mk', '.map', '.doc', '.tbl', '.bat', '.dat', '.gmm', '.naix', '.tmp', '.stdout', '.codebook', '.1st', '.lst']
path = os.path.dirname(__file__) ; listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk(path):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]
if args["logger"] == True: 
    logging.basicConfig(filename=path+"\log.txt", filemode='a', level=logging.INFO, encoding=encodings[1])

# FUNCS #########################################
def setPattern(x): 
    verStr = bytes(str(x), encoding=encodings[1])
    patternVer = re.compile(verStr + b'\nlog\n@(.*?)@\ntext\n@(.*?)@\n\n', re.DOTALL)
    return patternVer
patternVer = setPattern(args["version"])

def writeFile(ver): # open the file as binary data and attempt a regex search
        with open(currFile, "rb") as file: 
                data = bytearray(file.read()) ; new_data = re.search(patternVer, data)
        loggerText = ('\nGetting version: {}. Most recent: {}\nFileType: {}, Path:{}'.format(ver, fileCurrVer, currMime, currFile))
        if new_data == None: return
        else: new_data = (new_data.group(2)).replace(b'@@', b'@') # isolate new data, fix the double @@'s
        if currMime == "text": new_data = new_data[:-1] # fix for text files and trailing @ character

        # making sure dirs exist
        newFile = currFile[:len(path) +1] +"v"+ str(ver) + currFile[len(path):]
        if args["testrun"] == False: # Write the data to disk
            os.makedirs(os.path.dirname(newFile), exist_ok=True)    
            with open(newFile, "wb") as file: file.write(new_data)
        if args["logger"] == True and args["testrun"] == False: loggerText += "\nWrote file.\n"
        logging.info(loggerText)

# MAIN PROGRAM #########################################
for currFile in listOfFiles:
        # Get list of all ver no. in current file
        with open(currFile, "r", encoding=encodings[0]) as file: 
            fileCurrVer = re.sub("[;\n\t]", "", file.readline().strip("head")).split('.')
            dataTemp = file.read()
        if fileCurrVer[0] != '1': print("\nNothing to do for", currFile) ; continue
        fileCurrVer = ".".join(fileCurrVer)
        verList = [fileCurrVer]
        verList.extend(re.findall("next	([0-9].*);",dataTemp))
        #print(verList)
        try: # try determine filetype 
            if currFile.endswith(",v"): currFile[:-2]
            currMime = str((mimetypes.guess_type(currFile))[0])[:4] 
            if currMime == "None": # help out the mime with filetypes
                for ext in extensionsText:
                        if currFile.endswith(ext): currMime = 'text'
                for ext2 in extensionsBin:
                        if currFile.endswith(ext2): currMime = ext2       
            if currFile.endswith('bat'): currMime = 'text'
            if currFile == os.path.realpath(__file__): print("\nSkipping file", currFile) ; continue
        except: print("Filetype error.") ; currMime = "None"

        if args["allfiles"] == True: # CHECK ARGS
            for x in verList: patternVer = setPattern(x) ; writeFile(x)
        elif args["recent"] == True:
            writeFile(fileCurrVer)
        else: writeFile(args["version"])
