from Tkinter import Tk
from tkFileDialog import askopenfilenames
import numpy as np
import matplotlib.pyplot as plt
import re
from numpy import genfromtxt



Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
files = askopenfilenames() # show an "Open" dialog box and return the path to the selected file
files = re.findall('\{(.*?)\}', files)
global namedic
namedic = {}

#print(filename)
#namedic{}
for index in files:
##    print(index.split("/")[-1][3])
    if (index.split("/")[-1][3] == 'C'):
        sn = index.split("/")[-1][0:3]
        tfile = index.rsplit("/", 1)[0] + '/' + sn + 'C_V.CSV'
        data = genfromtxt(tfile, delimiter=',')
        tfile = index.rsplit("/", 1)[0] + '/' + sn + 'V_S.CSV'
        data2 = genfromtxt(tfile, delimiter=',')
        data = np.append(data, data2[:,[2]], 1)

##    tmp = index.split("/")
##    namedic[index.split("/")[-1][0:3]] = index
##
##for