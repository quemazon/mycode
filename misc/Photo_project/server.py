# -*- coding: utf-8 -*-
"""
Created on Sun May 01 14:09:50 2016

@author: default
"""
import pickle
import serial
import time
import string
import random
import os

dir_web = '/home/pi/PhotoFloat/web/albums/'

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class session_class:
    def __init__(self):
        self.dir_org = id_generator()
        os.mkdir(dir_web + self.dir_org)
        self.dir_wm = id_generator()
        os.mkdir(dir_web + self.dir_wm)
        self.start_time = time.localtime()
        self.end_time = 200
        self.ID = id_generator()
        self.locked = 'y'

ser = serial.Serial(
    port='/dev/rfcomm0',
    timeout = 0
)

sessions = [session_class()]

def new_session():
    sessions.append(session_class())
    pickle.dump(sessions, open('/home/pi/sessions.db','wb'))
    send_session_id()
    
def acknowledge():
    ser.write('ack')

def print_ticket():
    ser.write('printed')
    
def send_session_id():
    ser.write(str(sessions[-1].ID))   

while True:
    command = ser.read()
    if command == 'r':
        send_session_id()
    if command == 'n':
        new_session()
    if command == 'a':
        acknowledge()
    if command == 'p':
        print_ticket()
    time.sleep(.25)
 
