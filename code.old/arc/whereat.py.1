#!/usr/bin/python3
from datetime import datetime
import serial
from serial.tools.list_ports import comports

# settings
interval = 'minute'   # minute hour or day

# which serial? first one
port = comports()[0].device
ser = serial.Serial(port, 19200, timeout=1)

def lookFor(key, lin, dic, ter='\r'):
  # look for key.word in lin.e using ter.minator, store in dic.tionary
  if isinstance(lin, bytes):
    lin = lin.decode()
  if key in lin:
    at1=lin.find('=')+1
    at2=lin.find(ter, at1)
    dic[key]=lin[at1:at2]
    return at2
  else:
    return 0

def getGPS(ser):
  """ parse GPS responses into dict """
  gps = dict()
  ser.write(b'at+pt\r')
  lines = ser.readlines()
  for l in lines:
    x = lookFor('Time', l, gps, ter='.')
  ser.write(b'at+pd\r')
  lines = ser.readlines()
  for l in lines:
    x = lookFor('Date', l, gps)
  ser.write(b'at+pl\r')
  lines = ser.readlines()
  for l in lines:
    x = lookFor('Lati', l, gps)
    x = lookFor('Long', l, gps)
    x = lookFor('Used', l, gps)
  return gps

# main
def main():
  """main loop"""
  global ser
  fName = ''
  # day of year
  interval="%j"
  day=datetime.now().strftime(interval)
  if f"{day}.log" != fName: 
    fName = f"{day}.log"
  with open(fName, "w") as outF:
    gps = getGPS(ser)
    o = f"{gps['Time']}, Lati:{gps['Lati']}, Long:{gps['Long']}\n"
    outF.write(o)

#main()

>>> dt=g['Date'].split('-')[0:2]
>>> tm=g['Time'].split(':')[0:2]
>>> tm
['19', '57']
>>> "{0:02}{1:02}_{2:02}{3:02}".format(*(dt+tm))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  ValueError: '=' alignment not allowed in string format specifier
  >>> dt
  ['01', '13']
  >>> "{0:02d}{1:02d}_{2:02d}{3:02d}".format(*(dt+tm))
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ValueError: Unknown format code 'd' for object of type 'str'
    >>> "{0}{1}_{2}{3}".format(*(dt+tm))
    '0113_1957'
    >>> "{0}{1}{2}{3}.log".format(*(dt+tm))
    '01131957.log'

