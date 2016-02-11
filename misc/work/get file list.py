#this generates a file list for the database and

# Import the os module, for the os.walk function
import os
import re
import pickle
from Tkinter import Tk
from tkFileDialog import asksaveasfilename
from tkFileDialog import askdirectory

global namedic
namedic = {}
# Set the directory you want to start from
#rootDir = u'X:/4E10/Lot 2 data/'
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
rootDir = askdirectory() +'/'# show an "Open" dialog box and return the path to the selected file
for dirName, subdirList, fileList in os.walk(rootDir):
    #print('Found directory: %s' % dirName)
    for fname in fileList:
        if re.match('[\d,3].*V.CSV', fname):
            fullname = dirName + u'/' +fname
            namedic[fname[0:3]] = fullname
            print('\t%s' % fullname)
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
file = asksaveasfilename() # show a "save" dialog box and return the path to the selected
pickle.dump(namedic, open(file, "wb"))
