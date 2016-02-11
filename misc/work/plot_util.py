from pylab import *
import matplotlib.pyplot as plt
import pickle

class L(object):
    def __init__(self, serial):
        serial = str(serial)
        namedic = pickle.load(open(u'X:/python scripts/shot_index', "rb"))
        self.file = namedic[serial]
        shot = self.file.split("/")[-1]
        self.sn = shot[0:3]
        from numpy import genfromtxt
        data = genfromtxt(self.file, delimiter=',')
        self.t = data[:,[0]]
        self.c = data[:,[1]]
        self.v = data[:,[2]]
              
def makeplot(num):
    plt.figure(num)

def loadshot(serial):
    serial = str(serial)
    namedic = pickle.load(open(u'X:/python scripts/shot_index', "rb"))
    tfile = namedic[serial]
    shot = tfile.split("/")[-1]
    sn = shot[0:3]
    from numpy import genfromtxt
    data = genfromtxt(tfile, delimiter=',')
    return data

def preplot(plot):
    ax1 = plot.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
    ax2 = ax1.twinx()
            
def v(plot, serial):
    #ax = plot.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
    #ax = plot.add_subplot()
    plot.axes[0].plot(serial.t,serial.v)
    plot.axes[0].autoscale()
    show(plot)

def pc(*args):
    files = get_file_list()
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
    for shot in args: 
        data = load_shot_2(shot, files)# For regular CSV files from excelitas
##        data = convert_dodo(shot, files)
        ax1.plot(data[:,[0]], data[:,[1]], label = shot)
    ax1.set_xlim(-2e-7,2e-6)
    ax1.set_ylim(ymin=-50)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Current')
    ax1.legend(loc=0)    #fig.legend()
    fig.show()
  
def pcv(*args):
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
    ax2 = ax1.twinx()
    for shot in args:
        data = loadshot(shot)
        ax1.plot(data[:,[0]], data[:,[1]], label = shot)
        ax2.plot(data[:,[0]], data[:,[2]])
    ax1.set_xlim(-2e-7,2e-6)
    ax1.set_ylim(ymin=-50)
    #ax1.set_ylim(-50, 800)
    ax2.set_xlim(-2e-7,2e-6)
    ax2.set_ylim(ymin=-50)
    #ax2.set_ylim(-50, 1200)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Current')
    ax2.set_ylabel('Voltage')
    ax1.legend(loc=0)    #fig.legend()
    fig.show()
  
def pcvr(*args):
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
    ax2 = ax1.twinx()
    tcolor = ['r', 'g', 'b', 'c', 'm', 'k', 'y']
    i = 0
    for shot in args:
        data = loadshot(shot)
        #ax1.plot(data[:,[0]], data[:,[1]], label = shot)
        ax1.plot(data[:,[0]], data[:,[1]], label = shot, color= tcolor[i])
        ax1.plot(data[:,[0]], data[:,[2]], color= tcolor[i])
        ax2.plot(data[:,[0]], data[:,[2]]/data[:,[1]], color= tcolor[i])
        i = i+1
    ax1.set_xlim(0,2e-6)
    ax1.set_ylim(ymin=-50)
    #ax1.set_ylim(-50, 800)
    ax2.set_xlim(0,2e-6)
    #ax2.set_ylim(ymin=-50)
    ax2.set_ylim(-.1, 3)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Current/Voltage')
    ax2.set_ylabel('Resistance')
    ax1.legend(loc=0)    #fig.legend()
    fig.show()
  
def pvc_old(time, voltage, current): 
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
    ax2 = ax1.twinx()
    ax1.plot(time, voltage, label = 'voltage')
    ax2.plot(time, current, 'r', label = 'current')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Voltage')
    ax2.set_ylabel('Current')
    ax1.legend(loc=0)    #fig.legend()
    fig.show()
 
def storescopefile(data, serial):
    from Tkinter import Tk
    from tkFileDialog import askdirectory
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askdirectory() +'/' + serial + 'C_V.CSV' # show an "Open" dialog box and return the path to the selected file
    import numpy
    numpy.savetxt(filename, data, delimiter=",")

def getlanltraces():
    import numpy as np
    from Tkinter import Tk
    from tkFileDialog import askopenfilename

    tmp= []
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    from numpy import genfromtxt
    tmp = genfromtxt(filename, delimiter=',')
    data = tmp[:,[3]]
    data = np.append(data, tmp[:,[4]]/0.0035 , axis=1)

    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    #from numpy import genfromtxt
    tmp = genfromtxt(filename, delimiter=',')
    data = np.append(data, tmp[:,[4]]*-100.0 , axis=1)
    return data

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
   
def easyplot(data):
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
    ax1.plot(data[:,[0]], data[:,[1]])
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Current')
    fig.show()


def plot2(data, data2):
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
    ax1.plot(data[:,[0]], data[:,[1]], data2[:,[0]], data2[:,[1]])
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Current')
    fig.show()

def plot_current(data):
    fig = plt.plot(data[:,[0]], data[:,[1]])
    ##fig.show()
    
def storescopefile(data, serial):
    from Tkinter import Tk
    from tkFileDialog import askdirectory
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askdirectory() +'/' + serial + 'C_V.CSV' # show an "Open" dialog box and return the path to the selected file
    import numpy
    numpy.savetxt(filename, data, delimiter=",")

def shotenergy(serial):
    data = loadshot(serial)
    power = data[:,[1]] * data[:,[2]]
    tmp = np.where(data[:,[0]] > 1.5e-6)[0][0]
    power = power[:tmp,[0]]    
    tmp = np.where(power >5000)
    start = tmp[0][0]
    end = tmp[0][-1]
    tmp = power[start:end,[0]]
    step = data[1][0] - data[0][0]
    area = np.sum(tmp) * step
    #area = trapz(power.reshape((1, power.shape[0])), dx=step)
    return area
    
def burstenergy(serial):
    data = loadshot(serial)
    power = data[:,[1]] * data[:,[2]]
    tmp = np.where(power >5000)
    start = tmp[0][0]
    end = data[:,[2]].argmax()
    tmp = power[start:end,[0]]
    step = data[1][0] - data[0][0]
    area = np.sum(tmp) * step
    #area = trapz(power.reshape((1, power.shape[0])), dx=step)
    return area
    
def plotone(serial):
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
    ax2 = ax1.twinx()
    data = loadshot(serial)
    ax1.plot(data[:,[0]], data[:,[1]], data[:,[0]], data[:,[2]], label = serial)
    power = data[:,[1]] * data[:,[2]]
    ax2.plot(data[:,[0]], power, '-r')
    tmp = np.where(data[:,[0]] > 1.5e-6)[0][0]
    power = power[:tmp,[0]]    
    ax1.set_xlim(-2e-7,2e-6)
    ax1.set_ylim(ymin=-50)
    #ax1.set_ylim(-50, 800)
    ax2.set_xlim(-2e-7,2e-6)
    ax2.set_ylim(ymin=-5000)
    #ax2.set_ylim(-50, 1200)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Current, Voltage')
    ax2.set_ylabel('Power')
    ax1.legend(loc=0)    #fig.legend()
    
    tmp = np.where(power >5000)
    start = tmp[0][0]
    start = (data[start][0], power[start]) 
    end = tmp[0][-1]
    end = (data[end][0], power[end])
    maxx = data[:,[2]].argmax()
    maxx = (data[maxx][0], power[maxx])

    ax2.annotate('start', xy=start, xytext=start,
        arrowprops=dict(facecolor='black', shrink=0.05),
        )
    ax2.annotate('end', xy=end, xytext=end,
        arrowprops=dict(facecolor='black', shrink=0.05),
        )
    ax2.annotate('burst', xy=maxx, xytext=maxx,
        arrowprops=dict(facecolor='black', shrink=0.05),
        )
    fig.show()
  
def plotr(serial):
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
    ax2 = ax1.twinx()
    data = loadshot(serial)
    ax1.plot(data[:,[0]], data[:,[1]], data[:,[0]], data[:,[2]], label = serial)
    res = data[:,[2]] / data[:,[1]]
    ax2.plot(data[:,[0]], res, '-r')
    ax1.set_xlim(-2e-7,2e-6)
    ax1.set_ylim(ymin=-50)
    #ax1.set_ylim(-50, 800)
    ax2.set_xlim(-2e-7,2e-6)
#    ax2.set_ylim(ymin=-5000)
    ax2.set_ylim(-.1, 1.5)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Current, Voltage')
    ax2.set_ylabel('Resistance')
    ax1.legend(loc=0)    #fig.legend()
    fig.show()

def load_csv():
    from Tkinter import Tk
    from tkFileDialog import askopenfilename
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    from numpy import genfromtxt
    data = genfromtxt(filename, delimiter=',')
    return data

def get_file_list():
    from Tkinter import Tk
    from tkFileDialog import askdirectory
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    file_list = get_filepaths(askdirectory()) # show an "Open" dialog box and return the path to the selected file
    return file_list
    

def load_shot_2(serial, files_list):
    serial = str(serial)
    for files in files_list:
#    for files in get_filepaths(u'D:/4E10 data'):
        if files.find(serial) != -1:
            tfile = files
    shot = tfile.split("/")[-1]
    from numpy import genfromtxt
    data = genfromtxt(tfile, delimiter=',')
    return data

def convert_dodo(serial, files_list):
    serial = str(serial)
    for files in files_list:
#    for files in get_filepaths(u'D:/4E10 data'):
        if files.find(serial) != -1:
            tfile = files
    from numpy import genfromtxt
    data = genfromtxt(tfile, delimiter=',', skip_header=19)
    data[:,[1]] *=-1.0
    zero = np.where(data[:,[1]]>25)[0][0]
    data[:,[0]] = linspace(zero*-1.0e-9, (15000-zero)*1e-9, num=15000).reshape(15000,1)
    return data

def get_filepaths(directory):
    import os
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

