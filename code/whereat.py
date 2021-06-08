#!/usr/bin/python3
# v2 Tue 02 Feb 2021 09:53:51 AM UTC
import time
import sys
import serial
from A3la import A3la 
from pprint import pprint
from importlib import reload

# settings
interval = 'minute'   # minute hour or day

# which serial? first one
from serial.tools.list_ports import comports
port = comports()[0].device
ser = serial.Serial(port, 19200, timeout=1)
a3la = A3la(ser)

"""

while True:
  dtl = gps.getGPS()
  dt=g['Date'].split('-')[0:2]
  tm=g['Time'].split(':')[0:2]
  if not dt or not tm: 
    break
  with open(fName, "w") as outF:
    # "{0}{1}{2}{3}.log".format(*(dt+tm))
    o = f"{gps['Date']} {gps['Time']}, Lati:{gps['Lati']}, Long:{gps['Long']}\n"
    outF.write(o)
  """
