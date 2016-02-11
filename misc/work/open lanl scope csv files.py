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
