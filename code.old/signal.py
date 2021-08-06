#!/usr/bin/python3
# v2 Tue 02 Feb 2021 09:53:51 AM UTC
import time
import sys
import serial
import A3la
import Gps
import Rud
from importlib import reload

# settings
interval = 60

# which serial? first one
from serial.tools.list_ports import comports
port = comports()[0].device
ser = serial.Serial(port, 19200, timeout=1)
a3la = A3la(ser)

