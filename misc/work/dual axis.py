from Tkinter import Tk
from tkFileDialog import askopenfilename
import numpy as np
import matplotlib.pyplot as plt

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
#print(filename)
from numpy import genfromtxt
data1 = genfromtxt(filename, delimiter=',')

fig, ax1 = plt.subplots()
#t = np.arange(0.01, 10.0, 0.01)
ax1.plot(data1[:,[0]], data1[:,[1]], 'b-')
ax1.set_xlabel('time (s)')
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('Current', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')

ax2 = ax1.twinx()
#s2 = np.sin(2*np.pi*t)
ax2.plot(data1[:,[0]], data1[:,[2]], 'r-')
ax2.set_ylabel('Voltage', color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
plt.show()

##plt.plot(data1[:,[0]], data1[:,[2]], data2[:,[0]], data2[:,[2]], data3[:,[0]], data3[:,[2]], data4[:,[0]], data4[:,[2]])
##plt.show()
