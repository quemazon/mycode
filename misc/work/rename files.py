#this generates a file list for the database and

# Import the os module, for the os.walk function
import os
import re
import pickle
from Tkinter import Tk
from tkFileDialog import asksaveasfilename
from tkFileDialog import askdirectory
from numpy import genfromtxt



global namedic
namedic = {}
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
rootDir = askdirectory() +'/'# show an "Open" dialog box and return the path to the selected file
# Set the directory you want to start from
#rootDir = u'X:/4E10/Lot 2 data/'
for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        if re.match('[\d,3].*V.CSV', fname):  #used this for some matching
        #if re.match('.*[\d,3].CSV', fname):
        #if re.match('.*[\d,3]V.CSV', fname):
            #newname = fname.split('.')[0][-3:] + 'C_V.CSV'
            #newname = fname.split('_')[2] + 'C_V.CSV'
            #newname = dirName  + newname
            oldname = dirName + fname
            newname = dirName + 'temp/' + fname
            data = genfromtxt(oldname, delimiter=',')
            tmp1 = data[:,[1]]
            tmp2 = data[:,[2]]
            data[:,[1]] = tmp2
            data[:,[2]] = tmp1
            import numpy
            numpy.savetxt(newname, data, delimiter=",")

            #direct = fname.rpartition('/')[0] + '/'
            #print(oldname)
            #print(newname)
            #os.rename(oldname, newname)
            #namedic[fname[0:3]] = fullname
            #print('\t%s' % fullname)
            print(oldname)
##file = asksaveasfilename() # show a "save" dialog box and return the path to the selected
##pickle.dump(namedic, open(file, "wb"))
