#!/usr/bin/python
#
import io
#
def sum(str):
  """rudics 16bit CRC (bytes str)"""
  accum=0
  mask=0x7FFFFFFF
  for b in str:
    accum |= b
    # python int will get huge - strip bit 16 (a&7F)<<1
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
#
def msg(str):
  """return blk:bytes for (str:bytes)"""
  l=len(str)+5
  b=l.to_bytes(2,'big')+b'T\x01\x01'+str
  cs=sum(b)
  blk=b'@@@'+cs.to_bytes(2,'big')+b
  return blk
#
h=b'LR01'+b'QUEH'
cs=sum(h)
hdr=b'???'+cs.to_bytes(2,'big')+h
blk=msg(b'Hello')
f=open("py.hdr","wb")
f.write(hdr)
f.close()
f=open("py.blk","wb")
f.write(blk)
f.close()


