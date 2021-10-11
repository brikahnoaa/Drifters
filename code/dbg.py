#!/usr/bin/python3
# v2 Tue 02 Feb 2021 09:53:51 AM UTC
import time
import sys
import os
import serial
import serial.tools.list_ports
import A3la
import Gps
import Rud
from pprint import pprint,pformat
from importlib import reload
interval = 600
retry=9
# which serial? first one
buoy = os.uname().nodename
port = serial.tools.list_ports.comports()[0].device
ser = serial.Serial(port, 19200, timeout=1)
a3la = A3la.A3la(ser)
gps = Gps.Gps(a3la)
rud = Rud.Rud(a3la, buoy)
print(buoy)
#
print('data=gps.query()')
import code
code.interact(local=locals())
