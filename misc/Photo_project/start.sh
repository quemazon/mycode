#!/bin/bash
sudo python /home/pi/airnef/airnefcmd.py --ipaddress 192.168.15.1 --slot second --realtimedownload afternormal --outputdir /home/pi/airnef/incoming > /tmp/airnef.log &
sudo sdptool add sp &
sleep 2
#sudo rfcomm watch /dev/rfcomm0 sudo python /home/pi/server.py > /tmp/server.log &
sudo rfcomm watch /dev/rfcomm0 /tmp/rfcomm0.log &
sudo python /home/pi/mover.py > /tmp/mover.log &
sudo python /home/pi/print_mon.py &