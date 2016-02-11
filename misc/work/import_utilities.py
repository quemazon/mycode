from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal as sig
from Tkinter import Tk
from tkFileDialog import askopenfilename, askdirectory
import tkMessageBox
import os
from numpy import genfromtxt

data_dir = 'C:/4E10 data main/DEV-3/parameter study waveforms' #use data_dir = askdirectory()

def import_wfm_current():
    
    cvr = .00514    
    import numpy as np
    from scipy import signal as sig
    from Tkinter import Tk
    from tkFileDialog import askopenfilename
    import os

    tmp= []
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    os.system('c:/temp/ConvertTekWfm \"' + filename + '\" /CSV c:/temp/temp.csv')
    from numpy import genfromtxt
    tmp = genfromtxt('c:/temp/temp.csv', delimiter=',')
    points = tmp[0,1]
    period = tmp[1,1]
    nyq = 0.5 / period
    wn = 20e6/nyq
    data = np.zeros((points, 4))   # this creates an array, 4 wide by # points
    b, a = sig.butter(2, wn)  # creates a butterworth filter
    filtered = sig.filtfilt(b, a, tmp[:,[4]].reshape(-1,))  # apply filter filtfilt
    data[:,[1]] = filtered.reshape(-1,1) / -cvr # reshape, apply CVR.
    data[:,[0]] = np.linspace(0,1,num=points).reshape(points,1)  # may be redundant
    #data[:,[1]] = sig.resample(tmp[:,[4]], points_new) / -cvr
    #data[:,[1]] -= np.average(data[1:200,1])
    zero = np.where(data[:,[1]]>50.0)[0][0]  # find position of current rise (>50)
    first = -period*zero #set calculate first point
    last = first + points * period
    data[:,[0]] = np.linspace(first, last, num=points).reshape(points,1) # creat time base
    data[:,[2]] = tmp[:,[4]] / -cvr
    di = np.gradient(data[:,[1]].reshape(-1,))
    data[:,[3]] = di.reshape(-1,1) 
    #plot(data[:,[0]], data[:,[1]])
    plot_rise(data)
    #print data[np.where(data[:,[1]]>400)[0][0],0] * 1.0e9
    #data = np.append(data, (tmp[:,[4]]), axis=1)
    ##data = np.append(data, (0-tmp[:,[4]]), axis=1)
    ##var=np.where(data[:,[1]] >50)[0][0]
    ##var=data[var][0]
    ##data[:,[0]] = data[:,[0]] - var
    return data

def plot_rise(data):
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
    ax2 = ax1.twinx()
    ax1.plot(data[:,[0]], data[:,[1]])
    ax1.plot(data[:,[0]], data[:,[2]])
    ax2.plot(data[:,[0]], data[:,[3]])
    #ax1.set_xlim(-1e-7,3e-7)
    #ax2.set_xlim(-1e-7,3e-7)
    ax1.set_ylim(ymin=-50)
    #ax1.set_title('800V, 24" Extension')
    tmp = data[np.where(data[:,[1]]>400)[0][0],0]
    txt = str(tmp*1.0e9) + ' ns'
    #ax1.annotate(txt, xy=(tmp,400), xytext=(tmp-2.0e-7,400+25),
    #    arrowprops=dict(facecolor='black', shrink=0.05),
    #    )
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Current')
    fig.show()

def imp(*args):

    global pathname
    global filename
    global first
    tmp= []
    tmp
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    pathname = filename.rsplit(".", 1)[0]

    if filename.split(".")[-1] == "wfm":
        os.system('c:/temp/ConvertTekWfm \"' + filename + '\" /CSV c:/temp/temp.csv')
        tmp = genfromtxt('c:/temp/temp.csv', delimiter=',')
        return import_tek(tmp)
    if filename.split(".")[-1] == "csv":
        f = open(filename, 'r')
        first = f.readline().split(",")[0]
        f.close()
        tmp = genfromtxt(filename, delimiter=',')
        print first
        if first == '"Record Length"':
            return import_tek(tmp)
        else:
            a = 5

def get_file_type(filename):
    if filename.split(".")[-1] == "wfm":
        return "wfm"
    if filename.split(".")[-1] == "csv":
        f = open(filename, 'r')
        first = f.readline().split(",")[0]
        f.close()
        tmp = genfromtxt(filename, delimiter=',')
        print first
        if first == '"Record Length"':
            return import_tek(tmp)
        else:
            a = 5

def import_tek():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    pathname = filename.rsplit(".", 1)[0]
    if filename.split(".")[-1] == "wfm":
        os.system('c:/temp/ConvertTekWfm \"' + filename + '\" /CSV c:/temp/temp.csv')
        tmp = genfromtxt('c:/temp/temp.csv', delimiter=',')
        return fix_tek(tmp)
    if filename.split(".")[-1] == "csv":
        f = open(filename, 'r')
        first = f.readline().split(",")[0]
        f.close()
        tmp = genfromtxt(filename, delimiter=',')
        print first
        if first == '"Record Length"':
            return fix_tek(tmp)
        else:
            a = 5

def fix_tek(tmp):        
    points = tmp[0,1]
    period = tmp[1,1]
    data = np.zeros((points, 2))
    data[:,[0]] = tmp[:,[3]]
    data[:,[1]] = tmp[:,[4]]
    return tmp[:,[4]].reshape(-1,), points, period, tmp[0][3]

def import_excelitas(column):
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    pathname = filename.rsplit(".", 1)[0]
    tmp = genfromtxt(filename, delimiter=',')
    points = tmp.shape[0]
    period = (tmp[-1][0] - tmp[0][0]) / (points -1.0)
    first = tmp[0][0]
    return tmp[:,[column]].reshape(-1,), points, period, first 

def smooth(data, period, cutoff):
    nyq = 0.5 / period
    wn = cutoff/nyq
    data = np.zeros((points, 4))
    b, a = sig.butter(2, wn)
    return sig.filtfilt(b, a, data.reshape(-1,))

class test_data(object):
    def __init__(self):
        self.cvr = .005
        self.a = 5
        self.c = current_waveform(self.cvr)
        self.original = current_waveform(self.cvr)
        self.v = voltage_waveform()
        self.s = switch_waveform()
        self.t = 3
        self.plot = plot_class(self)
        self.cutoff = 20e6
        self.import_current()
        self.filt_cur()

    def imp(*args):    
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        pathname = filename.rsplit(".", 1)[0]
    
        if filename.split(".")[-1] == "wfm":
            os.system('c:/temp/ConvertTekWfm \"' + filename + '\" /CSV c:/temp/temp.csv')
            tmp = genfromtxt('c:/temp/temp.csv', delimiter=',')
            return import_tek(tmp)
        if filename.split(".")[-1] == "csv":
            f = open(filename, 'r')
            first = f.readline().split(",")[0]
            f.close()
            tmp = genfromtxt(filename, delimiter=',')
            print first
            if first == '"Record Length"':
                return import_tek(tmp)
            else:
                a = 5
    def get_filename(self):
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        self.filename = askopenfilename(initialdir = data_dir) # show an "Open" dialog box and return the path to the selected file
        self.pathname = self.filename.rsplit(".", 1)[0]
        self.name = self.filename.rsplit("/", 1)[1].rsplit(".", 1)[0]
    
    def get_file_type(self):
        self.ext = self.filename.split(".")[-1].lower()
        if self.ext == "wfm":
            self.ftype = "wfm"
            return
        if self.ext == "csv":
            f = open(self.filename, 'r')
            first = f.readline().split(",")[0]
            f.close()
            if first == '"Record Length"':
                self.ftype = "lcsv"
                return
            else:
                self.ftype = "ecsv"
                return
        if self.ext == "txt":
            f = open(self.filename, 'r')
            t = f.readline().split(",")[-1]
            f.close()
            if t == 'Software Version\n':
                self.ftype = "dodo"
                return

    def open_file_as_csv(self):
        filename = self.filename
        print self.ext
        print self.ext == "wfm"
        if self.ext == "wfm":
            os.system('c:/temp/ConvertTekWfm \"' + filename + '\" /CSV c:/temp/temp.csv')
            filename = 'c:/temp/temp.csv'
        self.data = genfromtxt(filename, delimiter=',', skip_header=20)

    def import_current(self):
        self.import_waveform()
        if self.ftype == "wfm":
            self.c.data = self.data[:,[4]] / -self.cvr
            self.get_time_base(self.data[:,[3]])
            print "cvr applied"

        if self.ftype == "lcsv":
            self.c.data = self.data[:,[4]] / -self.cvr
            self.get_time_base(self.data[:,[3]])
            print "cvr applied"

        if self.ftype == "ecsv":
            self.c.data = self.data[:,[1]]
            self.get_time_base(self.data[:,[0]])

        if self.ftype == "dodo":
            self.c.data = -self.data[:,[1]]
            self.s.data = self.data[:,[2]]
            self.points = self.data.shape[0]
            self.period = 1.0e-9
            self.first = 0.0            
            self.convert_time_arange()
            print "also imported switch data!"

    def get_time_base(self, tmp):
        self.points = tmp.shape[0]
        self.period = (tmp[-1][0] - tmp[0][0]) / (self.points -1.0)
        self.first = tmp[0][0]
        self.convert_time_arange() 
            
    def convert_time_arange(self):
        self.time = [self.first, self.first+self.points*self.period, self.period]

    def import_waveform(self):
        self.get_filename()
        self.get_file_type()
        self.open_file_as_csv()
    
    def import_many(self):
        self.fig = plt.figure()
        self.ax1 = self.fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes        
        time = arange(self.data.shape[0])
        self.ax1.plot(time, self.data[:,[0]], label = 0, color= 'r')
        self.ax2 = self.ax1.twinx()
        self.ax2.plot(time, self.data[:,[1]], label = 1, color= 'g')
        self.ax3 = self.ax1.twinx()
        self.ax3.plot(time, self.data[:,[2]], label = 2, color= 'b')
        self.ax4 = self.ax1.twinx()
        self.ax4.plot(time, self.data[:,[3]], label = 3, color= 'c')
        self.ax5 = self.ax1.twinx()
        self.ax5.plot(time, self.data[:,[4]], label = 4, color= 'm')
        self.ax6 = self.ax1.twinx()
        self.ax6.plot(time, self.data[:,[5]], label = 5, color= 'k')
        self.ax1.legend(loc=0)    #fig.legend()
        self.fig.show()

    def filt_cur(self):
        self.original.data = self.c.data
        nyq = 0.5 / self.period
        #wn = 20e6/nyq
        wn = self.cutoff/nyq
        data = np.zeros((self.points, 4))   # this creates an array, 4 wide by # points
        b, a = sig.butter(2, wn)  # creates a butterworth filter
        filtered = sig.filtfilt(b, a, self.c.data.reshape(-1,))  # apply filter filtfilt
        self.c.data = filtered.reshape(-1,1) # / -cvr # reshape, apply CVR.
        zero = np.where(self.c.data>50.0)[0][0]  # find position of current rise (>50)
        self.first = -self.period*zero #set calculate first point
        self.time = [self.first, self.first+self.points*self.period, self.period]
        #last = self.first + self.points * self.period
        #data[:,[0]] = np.linspace(first, last, num=points).reshape(points,1) # creat time base
                    
class waveform:
    def __init__(self):
        self.data = []
        self.points = []
        self.period = []
        self.first = []
    def import_wfm(self):
        self.data, self.points, self.period, self.first = import_tek()
        self.time = [self.first, self.first+self.points*self.period, self.period]        
    def import_etc(self, column):
        #self.data = import_excelitas(column)       
        self.data, self.points, self.period, self.first = import_excelitas(column)
        self.time = [self.first, self.first+self.points*self.period, self.period]        
                        
class current_waveform(waveform):
    def __init__(self, cvr):
        self.cvr = cvr
    def appy_cvr(self):
        self.data = self.data/-1.0/self.cvr

class voltage_waveform(waveform):
    pass

class switch_waveform(waveform):
    pass
        
def read_wfm(filename):
    import os
    from numpy import genfromtxt
    os.system('c:/temp/ConvertTekWfm \"' + filename + '\" /CSV c:/temp/temp.csv')
    return genfromtxt('c:/temp/temp.csv', delimiter=',')

class plot_class():
    def __init__(self, parent):
        self.parent = parent
    def create(self):
        self.fig = plt.figure()
        self.ax1 = self.fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes        
        self.ax1.plot(arange(*self.parent.time), self.parent.c.data)
    def add_switch(self):
        self.ax2 = self.ax1.twinx()
        self.ax2.plot(arange(*self.parent.s.time), self.parent.s.data)
    def show(self):
        self.fig.show()
    def add(self, time, waveform):
        self.ax1.plot(time, waveform)

def pc(*args):
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # main axes
    for shot in args: 
        ax1.plot(arange(*shot.time)*1e6, shot.c.data, label=shot.name)
    ax1.set_xlim(-.1,.7)
    ax1.set_ylim(ymin=-50)
    ax1.set_xlabel('Time (us)')
    ax1.set_ylabel('Current (A)')
    ax1.legend(loc=0)    #fig.legend()
    fig.show()
