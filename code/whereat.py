#!/usr/bin/python3
# v2 Tue 02 Feb 2021 09:53:51 AM UTC
import time
import sys
import os
import serial
import serial.tools.list_ports
from A3la import A3la 
from Gps import Gps
from pprint import pprint
from importlib import reload

with open("pid", 'w') as pid:
  pid.write(str(os.getpid()))
# settings
# which serial? first one
port = serial.tools.list_ports.comports()[0].device
ser = serial.Serial(port, 19200, timeout=1)
a3la = A3la(ser)
gps = Gps(a3la)
# delete pid file to stop loop
while(os.path.isfile("pid")):
  time.sleep(120)
  data=gps.query()
  # make two datafiles, may be corrupted
  with open("data",'a') as datafile:
    pprint(data,stream=datafile)
  with open("data2",'a') as datafile:
    pprint(data,stream=datafile)
