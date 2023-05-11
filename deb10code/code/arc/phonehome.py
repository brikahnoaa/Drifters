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
#
def translate(s):
  """convert A3LA format lat/long to generic
     '44:37.2583 North' to '44.62080N' """
  parts=s.replace(':',' ').split()
  degree=float(parts[0])+float(parts[1])/60
  return "{:.5f}{}".format(degree, parts[2][0])
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
with open("pid", 'w') as pid:
  pid.write(str(os.getpid())+'\n')
# delete pid file to stop loop
#
while(os.path.isfile("pid")):
  data=gps.query()
  # make two datafiles, may be corrupted
  with open("data",'a') as datafile:
    pprint(data,stream=datafile)
  with open("data2",'a') as datafile:
    pprint(data,stream=datafile)
  # translate 
  lt=translate(data['Lati'])
  ln=translate(data['Long'])
  message='  {} {},{}\r{}'.format(buoy, lt, ln, pformat(data))
  #retry on failure(recursive)
  attempt=0
  success=False
  while not success:
    success = rud.call(message)
    if success: break
    attempt+=1
    if attempt>=retry:
      print('Call failed, giving up')
      break
    print('Call failed, try again [{}]'.format(attempt))
  time.sleep(interval)
