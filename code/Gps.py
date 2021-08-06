#!/usr/bin/python3
# v1 Wed 03 Feb 2021 12:39:35 PM UTC
# v2 Tue Jun  1 07:43:46 PDT 2021
# Read, store, transmit GPS location
##
class Gps:
  def __init__(self, a3la, log=""):
    self.a3la = a3la
    self.log = log
    # check log path
  #
  def query(self):
    """ query self.a3la GPS, parse responses into dict:data, return data """
    data = {}
    self.a3la.write('at+pt\r')
    l = self.a3la.readlines()
    data.update( self.keyval('Time', l, ter='.') )
    self.a3la.write('at+pd\r')
    l = self.a3la.readlines()
    data.update( self.keyval('Date', l) )
    self.a3la.write('at+pl\r')
    l = self.a3la.readlines()
    data.update( self.keyval('Lati', l) )
    data.update( self.keyval('Long', l) )
    data.update( self.keyval('Used', l) )
    #if self.log:
    #  with open(self.log, "a") as outF:
    #    for k in data.keys():
    return data
  #
  def keyval(self, key, lines, ter='\r'):
    """look for key in [lines], pair with string from '=' to ter.minator"""
    if isinstance(key, bytes):
      key = key.decode() # to str
    for line in lines:
      if key in line:
        at1=line.find('=') + 1 # 0 if not found
        at2=line.find(ter, at1) # -1 if not found
        return {key:line[at1:at2]}
    return {}
  ##

