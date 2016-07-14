import os
import time

while True:
   if not os.path.exists('/dev/rfcomm1'):
	os.system('sudo rfcomm connect /dev/rfcomm1 0F:03:E0:A2:22:D1')
   time.sleep(2)
