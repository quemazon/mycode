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
import json
import evdev
import shutil

dir_in = '/home/pi/airnef/incoming/'
dir_web = '/home/pi/PhotoFloat/web/albums/'
remote = evdev.InputDevice('/dev/input/event0')
sessions = []
sn = 56

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_session():
    global sn
    session = {}
    session['dir_org'] = id_generator()
    os.mkdir(dir_web + session['dir_org'])
    session['dir_wm'] = id_generator()
    os.mkdir(dir_web + session['dir_wm'])
    sn += 69
    if sn > 999:
        sn -= 1000
    session['ID'] = sn
    #session['ID'] = id_generator()
    session['start_time'] = time.localtime()
    session['locked'] = 'y'
    return session
        
#ser = serial.Serial(
#    port='/dev/rfcomm0',
#    timeout = 0
#)


def json_out():
    minus_time = []
    for session in sessions:
       minus_time.append({'ID':session['ID'], 'dir_org':session['dir_org'], 'dir_wm':session['dir_wm'], 'locked':session['locked']})
    with open('/tmp/sessions.json', 'w') as outfile:
       outfile.write("session = '")
       json.dump(minus_time, outfile)
       outfile.write("';")

def read_remote():
    gen = remote.read()
    try:
        for ev in gen:
            pass
        new_session()
        print_ticket()
        time.sleep(.5)
        gen = remote.read()
        try:
            for ev in gen:
                pass
        except IOError:
            pass
    except IOError:
        pass

def delete_all_photos():
    global sessions
    shutil.rmtree(dir_web)
    os.mkdir(dir_web)
    os.mkdir(dir_web + 'default')
    os.remove('/tmp/sessions.json')
    os.remove('/home/pi/sessions.db')
    sessions = None
    sessions = [create_session()]
    with open("/home/pi/sessions.db", "wb") as f:
        pickle.dump(sessions, f)
    json_out()

    
def new_session():
    global sessions
    sessions.append(create_session())
    with open("/home/pi/sessions.db", "wb") as f:
        pickle.dump(sessions, f)
    json_out()
    if os.path.exists('/dev/rfcomm0'):
        send_session_id()
    print sessions[-1]
    print 'cool'

def acknowledge():
    ser.write('ack')

def print_ticket():
    if os.path.exists('/dev/rfcomm1'):
        lpt = serial.Serial(
            port='/dev/rfcomm1',
            timeout = 0)
        tmp = "\x1D\x42\x00\x1B\x21\x00"
        tmp += 'CONNECT TO WIFI: FREE_PHOTOS\r\n'
        tmp += 'ENTER ID IN BROWSER:\r\n'
        lpt.write(tmp)
        lpt.write("\x1D\x42\x00\x1B\x21\x30")
        tmp = 'a'
        tmp += '{:03d}'.format(sessions[-1]['ID'])
        tmp += '/\r\n\r\n'
        lpt.write(tmp)
        #lpt.write('ID: ' + str(sessions[-1]['ID']) + '/\r\n')
        lpt.close()
    #ser.write('printed\r\n')
    
def send_session_id():
    ser = serial.Serial(
        port='/dev/rfcomm0',
        timeout = 0)
    ser.write(str(sessions[-1]['ID']))   
    ser.close()

def send_status():
    ser = serial.Serial(
        port='/dev/rfcomm0',
        timeout = 0)
    out = '{:03d}'.format(sessions[-1]['ID']) + ','
    tmp = '{:03d}'.format(len(os.listdir(dir_in)))
    out += tmp + ','
    #out += str(len(os.listdir(dir_in))) + ','
    tot = 0
    with open('/var/lib/misc/dnsmasq.leases' , 'r') as f:
        leases = f.read()
        leases = leases.split('\n')
        for i in leases:
            tot += len(i.split(' '))
    out += '{:03d}'.format(tot/2)
    if os.path.exists('/dev/rfcomm1'):
        out += ',p'
    else:
        out += ',n'
    out += '\r\n'
#    out += str(tot/2) + ','
#    counter = 20 - len(out)
#    for j in range(counter):
#        out += '0'
#    out += '\r\n'
    ser.write(out)
    ser.close()

def unlock_session():
    ser = serial.Serial(
        port='/dev/rfcomm0',
        timeout = 10)
    ser.write('?')
    response = int(ser.read(size=3))
    for session in sessions:
        if session['ID'] == response:
            session['locked'] = 'n'
            ser.write('{:03d}'.format(response))
            ser.close()
            return
    ser.write('000')
    ser.close()

if os.path.exists('/home/pi/sessions.db'):
    with open("/home/pi/sessions.db", "rb") as f:
        sessions = pickle.load(f)
        sn = sessions[-1]['ID']
else:
    sessions = [create_session()]
    with open("/home/pi/sessions.db", "wb") as f:
        pickle.dump(sessions, f)
if os.path.exists('/tmp/sessions.json'):
    os.remove('/tmp/sessions.json')
json_out()

while True:
    if os.path.exists('/dev/rfcomm0'):
        ser = serial.Serial(
            port='/dev/rfcomm0',
            timeout = 0)
        command = ser.read()
        if command == 'r':
            send_session_id()
        if command == 'n':
            new_session()
        if command == 'a':
            acknowledge()
        if command == 'p':
            print_ticket()
        if command == 's':
            send_status()
        if command == 'd':
            delete_all_photos()
        if command == 'u':
            unlock_session()
        ser.close()
        read_remote()
    time.sleep(.25)

 
