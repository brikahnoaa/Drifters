#!/usr/bin/python3
# v1 Wed 03 Feb 2021 12:39:35 PM UTC
# v2 Tue Jun  1 07:43:46 PDT 2021
# Read, store, transmit GPS location
##
def getGps(a3la):
  """ using a3la, parse GPS responses into dict """
  data = {}
  a3la.write('at+pt\r')
  l = a3la.readlines()
  data.update( a3la.lookFor('Time', l, ter='.') )
  a3la.write('at+pd\r')
  l = a3la.readlines()
  data.update( a3la.lookFor('Date', l) )
  a3la.write('at+pl\r')
  l = a3la.readlines()
  data.update( a3la.lookFor('Lati', l) )
  data.update( a3la.lookFor('Long', l) )
  data.update( a3la.lookFor('Used', l) )
  return data
##
def send(a3la, buff):
  """ use a3la to send rudics message """
