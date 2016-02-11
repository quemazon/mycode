from Tkinter import Tk
from tkFileDialog import askopenfilename
import csv

tmp= []
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
with open(filename, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        print row
        tmp.append(row)

