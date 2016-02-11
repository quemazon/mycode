class LoadData(object):
    def __init__(self, serial):
        try:
            namedic
        except NameError:
            import pickle
            from Tkinter import Tk
            from tkFileDialog import askopenfilename
            Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
            file = askopenfilename() # show an "Open" dialog box and return the path to the selected file
            global namedic
            namedic = pickle.load(open(file, "rb"))
        self.file = namedic[serial]
        shot = self.file.split("/")[-1]
        self.sn = shot[0:3]
        from numpy import genfromtxt
        data = genfromtxt(self.file, delimiter=',')
        self.t = data[:,[0]]
        self.c = data[:,[1]]
        self.v = data[:,[2]]

