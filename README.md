# CVS-attic-checkout

Scripts to restore deleted files within the Attic folders from certain CVS repos.

Copies all folders + files while preserving folder hierarchy.

It removes the heading and tailing CVS info from files, 

and extracts the data based on the version numbers within each file

# Step 1: 

# Extract the attic files from a repo using atticExtract.py

Make a list of directories to copy in "attics.txt"

For example: 
  
          find . -iname "attic*" > attics.txt
  
Place "atticExtract.py" and "attics.txt" in a directory containing the repo, and run the script.

# Step 2: 

# Process & grab different versions of files using atticGrabber.py

Place "atticGrabber.py" script in folder containing the repo, and run it.

Check the "ARGUMENTS" section for info on how the script can be run. For exapmple:

Grab every version of every file:     

      ./atticGrabber.py -a True
                                    
      ./atticGrabber.py --all True
                                       
Grab ONLY v1.2 files:                 

      ./atticGrabber.py -v 1.2

Do a full dry run, with logging:      

      ./atticGrabber.py -l True -t True -a True

Grab ONLY most recent files:          

      ./atticGrabber.py -r True
