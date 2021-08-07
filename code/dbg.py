#!/usr/bin/python3
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
import code

interval = 120

port = serial.tools.list_ports.comports()[0].device
buoyname = os.uname().nodename
ser = serial.Serial(port, 19200, timeout=1)
a3la = A3la.A3la(ser)
gps = Gps.Gps(a3la)
rud = Rud.Rud(a3la)
print('data=gps.query()')
code.interact(local=locals())
