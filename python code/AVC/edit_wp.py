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
def callback():
    print "click!"
    print e.get()

def openserial(port):
    global ser
    ser = serial.Serial(port, 115200, timeout=5)

def closeserial():
    ser.close()

class DataSet():
    def __init__(self):
        self.wpx = zeros(21, float)
        self.wpy = zeros(21, float)
        self.x = array([])
        self.y = array([])
        self.speed = array([])
        self.gyro = array([])
        self.accel = array([])
        self.steer = array([])
        self.angle = array([])
        self.proximity = array([])
        self.dist = array([])
        self.angle_diff = array([])
        self.par_WAYPOINT_ACCEPT = None
        self.par_S1 = None
        self.par_S2 = None
        self.par_S3 = None
        self.par_S4 = None
        self.par_SB = None
        self.par_P1 = None
        self.par_P2 = None
        self.par_P3 = None
        self.par_BREAKING_SPEED = None
        self.par_L1 = None
        self.par_L2 = None
        self.par_L3 = None
        self.par_L4 = None
        self.par_PATH_FOLLOWING = None
        self.par_LOOK_AHEAD = None
        self.par_GYRO_CAL = None
        self.par_STEER_ADJUST = None
        self.par_SERVO_LIM = None
        self.par_STEER_GAIN = None
        self.par_SPEED_TOGGLE_ANGLE = None
        self.par_CLICK_INCHES = None

def wait_init():
    while True:
        temp = ser.readline()
        print temp
        if temp.find("initialize") != -1:
            break

def get_data():
    wait_init();
    first = 0
    while True:  # make this break when serial times out
        temp = ser.readline()
        if len(temp) < 2 :
            temp = "timeout"
            if first == 1:
                break
        if temp[0] == "$":
            temp = temp[1:].split(",")
            for item in temp:
                print item
                #print item to window
        elif temp[0] == "#":
            temp = temp[1:].split(",")
            wp = int(temp[0])
            d.wpx[wp] = float(temp[1])
            d.wpy[wp] = float(temp[2])
            #plot coordinate on graph, add to databas?
        elif temp[0] == "d":
            first = 1
            temp = temp[1:].split(",")
            d.x = append(d.x, array([float(temp[0])]))
            d.y = append(d.y, array([float(temp[1])]))
            d.speed = append(d.speed, array([float(temp[2])]))
            d.gyro = append(d.gyro, array([float(temp[3])]))
            d.accel = append(d.accel, array([float(temp[4])]))
            d.steer = append(d.steer, array([float(temp[5])]))
            d.angle = append(d.angle, array([float(temp[6])]))
            d.proximity = append(d.proximity, array([float(temp[7])]))
            d.angle_diff = append(d.angle_diff, array([float(temp[8])]))
        elif temp[0] == "p":
            temp = temp[1:].split(",")
            d.par_WAYPOINT_ACCEPT = int(temp[0])
            d.par_S1 = int(temp[1])
            d.par_S2 = int(temp[2])
            d.par_S3 = int(temp[3])
            d.par_S4 = int(temp[4])
            d.par_SB = int(temp[5])
            d.par_P1 = int(temp[6])
            d.par_P2 = int(temp[7])
            d.par_P3 = int(temp[8])
            d.par_BREAKING_SPEED = int(temp[9])
            d.par_L1 = int(temp[10])
            d.par_L2 = int(temp[11])
            d.par_L3 = int(temp[12])
            d.par_L4 = int(temp[13])
            d.par_PATH_FOLLOWING = int(temp[14])
            d.par_LOOK_AHEAD = int(temp[15])
            d.par_GYRO_CAL = int(temp[16])
            d.par_STEER_ADJUST = int(temp[17])
            d.par_SERVO_LIM = int(temp[18])
            d.par_STEER_GAIN = float(temp[19])
            d.par_SPEED_TOGGLE_ANGLE = float(temp[20])
            d.par_CLICK_INCHES = float(temp[21])
            print "got parameters"

    ser.close()
    d.dist = arange(0, len(d.x), 1)
    d.dist = d.dist *2.33
    d.accel = -d.accel

def filter_data():
    import numpy as np
    d.speed = np.convolve(d.speed, np.ones(4)/4, "same")
    d.accel = np.convolve(d.accel, np.ones(10)/10, "same")
    plot_data()

# print coordinates plot, mark waypoints, draw LOS lines
# possilbly color by speed

# plot: rates for accel and gyro, speed, angle

# save final result to png file for now
#maybe try to picle everything. and save to file.

def plot_data():

    from mpl_toolkits.axes_grid1 import host_subplot
    import mpl_toolkits.axisartist as AA
    import matplotlib.pyplot as plt

    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)

    par1 = host.twinx()
    par2 = host.twinx()
    par3 = host.twinx()
    par4 = host.twinx()
    par5 = host.twinx()

    offset = 60
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par2,
                                        offset=(offset, 0))
    par2.axis["right"].toggle(all=True)

    new_fixed_axis = par3.get_grid_helper().new_fixed_axis
    par3.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par3,
                                        offset=(offset*2, 0))
    par3.axis["right"].toggle(all=True)

    new_fixed_axis = par4.get_grid_helper().new_fixed_axis
    par4.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par4,
                                        offset=(offset*3, 0))
    par4.axis["right"].toggle(all=True)

    new_fixed_axis = par5.get_grid_helper().new_fixed_axis
    par5.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par5,
                                        offset=(offset*4, 0))
    par5.axis["right"].toggle(all=True)


    #host.set_xlim(0, 2)
    #host.set_ylim(0, 2)

    host.set_xlabel("Distance")
    host.set_ylabel("Speed")
    par1.set_ylabel("Turn rate")
    par2.set_ylabel("Lateral Accel")
    par3.set_ylabel("Angle")
    par4.set_ylabel("Steering")
    par5.set_ylabel("Proximity")

    p1, = host.plot(d.dist, d.speed, label="Speed")
    p2, = par1.plot(d.dist, d.gyro, label="Turn Rate")
    p3, = par2.plot(d.dist, d.accel, label="Lateral Accel")
    p4, = par3.plot(d.dist, d.angle, label="Angle")
    p5, = par4.plot(d.dist, d.steer, label="Steering")
    p6, = par5.plot(d.dist, d.proximity, label="Proximity")

    #par1.set_ylim(0, 4)
    #par2.set_ylim(1, 65)

    host.legend()

    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    par2.axis["right"].label.set_color(p3.get_color())
    par3.axis["right"].label.set_color(p4.get_color())
    par4.axis["right"].label.set_color(p5.get_color())
    par5.axis["right"].label.set_color(p6.get_color())

    plt.draw()
    plt.show()

def plot_xy(data):
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

def save_file(data):
    import pickle
    from tkFileDialog import asksaveasfilename
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = asksaveasfilename()
    pickle.dump(data, open(filename, "wb" ))

def load_file():
    import pickle
    from tkFileDialog import askopenfilename
    filename = askopenfilename()
    return pickle.load(open(filename, "rb"))

def export_wp(wps):
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
        
             
def read_wp():
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
