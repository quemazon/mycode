#!/bin/sh
sudo python /home/pi/airnef/airnefcmd.py --slot second --realtimedownload afternormal --outputdir /home/pi/airnef/incoming > /tmp/airnef.log &
sudo sdptool add sp &
sleep 2
sudo rfcomm watch /dev/rfcomm0 sudo python /home/pi/server.py > /tmp/server.log &
sudo python /home/pi/mover.py > /tmp/mover.log &

