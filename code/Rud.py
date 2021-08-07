#!/usr/bin/python3
# Send message via rudics
import sys
import A3la
##
class Rud:
  ##
  def __init__(self, a3la):
    self.a3la=a3la
  def crc(self, barr):
    """xmodem CRC (bytearray barr)"""
    accum=0
    mask=0x7FFFFFFF
    for b in barr:
      accum |= b
      # python int will get huge - strip to 15 bits (a&7F)<<1
      for i in range(0,8):
        accum = (accum & mask) << 1
        if (accum & 0x01000000):
          accum ^= 0x00102100
    # xmodem dumb
    for i in range(0,2):
      # accum |= 0
      for i in range(0,8):
        accum = (accum & mask) << 1
        if (accum & 0x01000000):
          accum ^= 0x00102100
    return  ((accum >> 8) & 0xFFFF)
  ##
  def call(self, mesg):
    """call home and send (byte/array mesg)"""
    if isinstance(mesg, str):
      mesg = mesg.encode() # to bytes
    a3la = self.a3la
    prj = b'LR01'+b'QUEH'
    cs = self.crc(prj).to_bytes(2,'big')
    projHdr = bytes(b'???'+cs+prj)
    ln = (len(mesg)+5).to_bytes(2,'big')
    blk = bytes(ln+b'T\x01\x01'+mesg)
    cs = self.crc(blk).to_bytes(2,'big')
    mesgBlk = bytes(b'@@@'+cs+blk)
    # start call
    try:
      a3la.writeln('at+cpas')
      a3la.expect('OK')
      a3la.writeln('at+chup')
      a3la.expect('OK')
      a3la.writeln('atd'+'0088160000519')
      a3la.expect('CONNECT', wait=15)
      a3la.write(projHdr)
      a3la.expect('ACK', wait=20)
      a3la.write(mesgBlk)
      a3la.expect('done', wait=20)
    except:
      import traceback
      traceback.print_exc(limit=1)
      return(False)
    return(True)
