#!/usr/bin/python3
# v2 Tue 02 Feb 2021 09:53:51 AM UTC
import time
import sys
import serial
from Gps import Gps
from importlib import reload
#
# settings
#
# which serial? first one
from serial.tools.list_ports import comports
port = comports()[0].device
ser = serial.Serial(port, 19200, timeout=1)
gps = Gps(ser)
#
def crc(barr):
  """xmodem CRC (bytearray barr)"""
  accum=0
  mask=0x7FFFFFFF
  for b in barr:
    accum |= b
    # python int will get huge - strip high bit 16 (a&7F)<<1
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

def call(mesg):
  """call home and send (byte/array mesg)"""
  proj = b'LR01'+b'QUEH'
  cs = crc(proj).to_bytes(2,'big')
  projHdr = bytearray(b'???'+cs+proj)
  

'''

  flogf(" %s", utlTime());
  utlWrite(irid.port, "at+cpas", EOL);
  if (!utlReadExpect(irid.port, all.str, "OK", 5)) return 2;
  utlWrite(irid.port, "at+clcc", EOL);
  if (!utlReadExpect(irid.port, all.str, "OK", 5)) return 3;
  utlMatchAfter(str, all.str, "+CLCC:", "0123456789");
  if (!strcmp(str, "006")==0) {
    utlWrite(irid.port, "at+chup", EOL);
    if (!utlReadExpect(irid.port, all.str, "OK", 5)) return 4;
  }
  utlRead(irid.port, all.str); // flush
  sprintf(str, "atd%s", iri.phoneNum);
  // dial
  for (i=0; i<iri.redial; i++) {
    utlWrite(irid.port, str, EOL);
    utlReadWait(irid.port, all.str, CALL_DELAY);
    DBG1("%s", all.str);
    if (strstr(all.str, "CONNECT 9600")) {
      flogf("\nCONNECTED@~%d %ldus", iri.baud, irid.usec);
      return 0;
    }
    flogf(" (%d)", i);
    utlNap(3);
  }
  utlErr(iri_err, "call retry exceeded");
  return 4;
} // iriDial

///
// send proj hdr followed by "Hello", catch landResponse
// rets: *resp<-landResp 1=retries 2=noCarrier +10=landResp +20=landCmds
// sets: irid.buf
int iriProjHello(uchar *resp) {
  static char *self="iriProjHello";
  static char *rets="1=retries 2=noCarrier +10=landResp +20=landCmds";
  int r, try, hdr=13;
  char *s=NULL;
  try = iri.hdrTry;
  while (!s) {
    if (try-- <= 0) raise(1);
    flogf(" projHdr");
    iriSendSlow(irid.projHdr, hdr);
    s = utlReadExpect(irid.port, all.str, "ACK", iri.hdrResp);
    if (strstr(all.str, "NO CARRIER")) raise(2);
  }
  flogf(" hello");
  sprintf(irid.block, "hello");
  iriSendBlock(5, 1, 1);
  if ((r = iriLandResp(resp))) raise(10+r);
  if (strstr(resp, "cmds")) {
    if ((r = iriLandCmds(resp))) raise(20+r);
    iriProcessCmds(resp);
  }
  return 0;
} // iriProjHello


///
// 3 bytes of leader which will be @@@; (three bytes of 0x40); 
// 2 bytes of crc checksum;
// 2 bytes of message length;
// 1 byte of message type;  (‘T’ or ‘I’ =Text,‘B’= Binary, ‘Z’ = Zip 
// 1 byte block number;
// 1 byte number of blocks.
// irid.block already contains msg
// uses: irid.buf .block iri.
int iriSendBlock(int bsiz, int bnum, int btot) {
  static char *self="iriSendBlock";
  static char *rets="1=inFromLand";
  int cs, size;
  DBG0("%s(%d,%d,%d)", self, bsiz, bnum, btot);
  // make hdr - beware null terminated sprintf, use memcpy
  size = bsiz+IRID_BUF_BLK-IRID_BUF_SUB;
  sprintf(all.str, "@@@CS%c%cT%c%c", 
    (char) (size>>8 & 0xFF), (char) (size & 0xFF), 
    (char) bnum, (char) btot);
  memcpy(irid.buf, all.str, IRID_BUF_BLK);
  // poke in cs high and low bytes
  cs = iriCRC(irid.buf+IRID_BUF_SUB, size);
  irid.buf[IRID_BUF_CS] = (char) (cs>>8 & 0xFF);
  irid.buf[IRID_BUF_CS+1] = (char) (cs & 0xFF);
  flogf(" %d/%d", bnum, btot);
  // send 
  if (TURxQueuedCount(irid.port)) raise(1); // junk in the trunk?
  iriSendSlow(irid.buf, bsiz+IRID_BUF_BLK); 
  if (irid.log) write(irid.log, irid.block, (long) bsiz);
  return 0;
} // iriSendBlock
'''
