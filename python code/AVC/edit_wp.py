# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 21:09:47 2016

@author: default
"""

#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      default
#
# Created:     14/05/2014
# Copyright:   (c) default 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import serial
#from sys import exit
from random import *
from pylab import*
from Tkinter import *
from time import sleep

#def os(port):
#    global ser
#    ser = serial.Serial(port, 115200, timeout=5)
#
def cs():
    ser.close()

def gw(data):   #graph waypoints
    import matplotlib.pyplot as plt
    #t = arange(0.0, 2.0, 0.01)
    #s = sin(2*pi*t)
    x = []
    y = []
    pt = []
    for counter, value in enumerate(data):
       x.append(value[0])
       y.append(value[1])
       pt.append(counter)
    plt.plot(x, y, 'o')
    for i in pt:
    #(x, y) = DATA[i]
    #(dd, dl, r, dr, dp) = dash_style[i]
    #print('dashlen call %d' % dl)
        plt.text(x[i]+3, y[i]+3, str(i))


    title('X, Y Inches')
    grid(True)
    show()

def wf(data):   # write file
    import pickle
    from tkFileDialog import asksaveasfilename
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = asksaveasfilename()
    pickle.dump(data, open(filename, "wb" ))

def rf():       # read file
    import pickle
    from tkFileDialog import askopenfilename
    filename = askopenfilename()
    return pickle.load(open(filename, "rb"))

def ww(wps):    #write waypoint
    wps = wps[:20]
    ser.flushOutput()
    ser.write('@')
    sleep(.3)
    for i in wps:
        ser.write(str(i[0]))
        ser.write('!')
        ser.write(str(i[1]))
        ser.write('!')
        ser.write(str(i[2]))
        ser.write('!')
ser    
def rw():   #read waypoint
#    ser = serial.Serial(9, 115200, timeout=5)
    ser.flushInput()
    ser.write('#')
    biglist = ser.readline().split(';')
    biglist = biglist[:20] #delet last element, which isn't a wp
    #print tmp1
    #return tmp1
    wps = []
    for i in arange(20):
        individual = biglist[i].split(',')
        tmp = []
        tmp.append(int(float(individual[0])))
        tmp.append(int(float(individual[1])))
        tmp.append(int(individual[2]))
        wps.append(tmp)        
 #   ser.close()
    return wps

def pw(wps):
    for i, j in enumerate(wps):
        print i, j
        
