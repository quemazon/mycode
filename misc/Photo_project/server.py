# -*- coding: utf-8 -*-
"""
Created on Sun May 01 14:09:50 2016

@author: default
"""

import serial
from time import sleep

dir_in = '/home/pi/airnef/incoming/'
dir_web = '/home/pi/PhotoFloat/web/albums/'

class session_class:
    def __init__(self, num):
        self.dir_org = dir_web + 'originals/'
        self.dir_wm = dir_web + 'watermarked/'
        self.start_time = 100
        self.end_time = 200
        self.ID = num
        self.locked = 'y'

ser = serial.Serial(
    port='/dev/rfcomm0',
    timeout = 0
)

sessions = [session_class(1)]

def new_session():
    sessions.append(session_class(sessions[-1].ID + 1))
    send_session_id()
    
def acknowledge():
    ser.write('ack')

def print_ticket():
    ser.write('printed')
    
def send_session_id():
    ser.write(str(sessions[-1].ID))    

while True:
    command = ser.read()
    if command == 'i':
        send_session_id()
    if command == 'n':
        new_session()
    if command == 'a':
        acknowledge()
    if command == 'p':
        print_ticket()
    sleep(.25)
 
