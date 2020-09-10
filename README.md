# CVS-attic-checkout

Scripts to restore deleted files within the Attic folders from certain CVS repos.

Copies all folders + files while preserving folder hierarchy.

It removes the heading and tailing CVS info from files, 

and extracts the data based on the version numbers within each file

# Step 1: Extract attic files from repo using atticExtract.py

Make a list of directories to copy in "attics.txt".

For example: 
  
          find . -iname "attic*" > attics.txt
  
Refer to the provided attics.txt for an example of how it should look.

Place "atticExtract.py" and "attics.txt" in a directory containing the repo, and run the script.

# Step 2: Grab data from files using atticGrabber.py

Use a bulk renamer to remove all ",v" from filenames, like PowerRename for example.

Place "atticGrabber.py" script in folder containing the repo, and run it.

Check the "ARGUMENTS" section for info on different ways the script can be run. For example:
                                       
Grab ONLY v1.2 files:                 

      python ./atticGrabber.py -v 1.2

Do a full dry run:      

      python ./atticGrabber.py -t true

Grab ONLY most recent files, with no log file:          

      python ./atticGrabber.py -r true -l false
