#!/usr/bin/python3
# v2 Tue 02 Feb 2021 09:53:51 AM UTC
import time
import sys
import os
import serial
from A3la import A3la 
from Gps import Gps
from pprint import pprint
from importlib import reload
#
with open("pid", 'w') as pid:
  pid.write(str(os.getpid()))
#
# settings
#
# which serial? first one
port = serial.tools.list_ports.comports()[0].device
ser = serial.Serial(port, 19200, timeout=1)
a3la = A3la(ser)
gps = Gps(a3la,"gps.log")
# delete pid file to stop loop
while(os.path.isfile("pid")):
  time.sleep(120)
  data=gps.query()
  with open("data",'a') as data
    pprint(data,stream=datafile)
