#!/usr/bin/python3
# class A3la
import serial
from time import sleep

class ExpectError(KeyError): pass
class A3la:
  """A3la (gps&iri) communications"""
  def __init__(self, ser, log=""):
    self.ser=ser
    self.log=log
  ##
  def write(self, line):
    """write to serial"""
    if isinstance(line, str):
      line = line.encode() # to bytes
    self.ser.write(line)
  ##
  def writeln(self, line):
    """write to serial"""
    if isinstance(line, str):
      line = line.encode() # to bytes
    self.write(line+b'\r')
  ##
  def readlines(self):
    """read from serial, maybe log
       return [str]"""
    lines = [ l.decode() for l in self.ser.readlines() ] # [str]
    if self.log:
      with open(self.log, "a") as outF:
        for l in lines:
          outF.write(l)
    return lines
  ##
  def expect(self, key, wait=5):
    """ consume response, look for 'phrase' """
    if isinstance(key, bytes):
      key = key.decode() # to str
    # wait seconds for key
    for i in range(wait):
      lines = self.readlines()
      for l in lines:
        if key in l: return(True)
      sleep(1)
    raise ExpectError
  ##
  def expectlines(self, key, wait=5):
    """ consume response, look for 'key', return all """
    if isinstance(key, bytes):
      key = key.decode() # to str
    # wait seconds for key
    lines = []
    for i in range(wait):
      lines += self.readlines()
      for l in lines:
        if key in l: return(lines)
      sleep(1)
    raise ExpectError
  ##
