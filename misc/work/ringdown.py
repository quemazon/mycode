from pylab import *
import matplotlib.pyplot as plt
import pickle

def readwfm():
    import numpy as np
    from Tkinter import Tk
    from tkFileDialog import askopenfilename
    import os

    tmp= []
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    os.system('c:/temp/ConvertTekWfm \"' + filename + '\" /CSV c:/temp/temp.csv')
    from numpy import genfromtxt
    tmp = genfromtxt('c:/temp/temp.csv', delimiter=',')
    data = tmp[:,[3]]
    data = np.append(data, (tmp[:,[4]]), axis=1)
    ##data = np.append(data, (0-tmp[:,[4]]), axis=1)
    ##var=np.where(data[:,[1]] >50)[0][0]
    ##var=data[var][0]
    ##data[:,[0]] = data[:,[0]] - var
    return data
 
def ring(cvr):
    data = readwfm()
    data[:,1] = data[:,1]/cvr  ## CVR value here
    ##data[:,1] = data[:,1]/-.004894  ## CVR value here
    data[:,1] = np.convolve(data[:,1], np.ones(100)/100, mode='same') #averaging filter
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
    ax1.plot(data[:,0], data[:,1])
    step = (data[-1,0] - data[0,0]) / len(data)
    maxx = data[:,1].argmax()
    ten = np.where(data[:,1] > data[maxx,1]*.1)[0][0]
    ninety = np.where(data[:,1] > data[maxx,1]*.9)[0][0]
    rise = (ninety - ten)*step*1e9
    print "rise time: ", rise, " ns"
    print "max current: ", data[maxx,1], " A"
    ax1.annotate('90%', xy=(data[ninety,0], data[ninety,1]),
        xycoords='data', xytext=(-50,30),
        textcoords='offset points', arrowprops=dict(arrowstyle="->"))
    ax1.annotate('10%', xy=(data[ten,0], data[ten,1]),
        xycoords='data', xytext=(-50,30),
        textcoords='offset points', arrowprops=dict(arrowstyle="->"))
    ax1.annotate('Max', xy=(data[maxx,0], data[maxx,1]),
        xycoords='data', xytext=(-50,30),
        textcoords='offset points', arrowprops=dict(arrowstyle="->"))
    fig.show()


