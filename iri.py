  // set projHdr to 13 char project header, 0 in byte 14
  // poke in checksum high and low bytes
  sprintf(irid.projHdr, "???cs%4s%4s", iri.project, iri.platform);
  cs = iriCRC(irid.projHdr+5, 8);
  irid.projHdr[3] = (char) (cs >> 8) & 0xFF;
  irid.projHdr[4] = (char) (cs & 0xFF);

int iriCRC(uchar *buf, int cnt) {
  long accum=0x00000000;
  int i, j;
  static char *self="iriCRC";
  DBG();
  if (cnt <= 0) return 0;
  while (cnt--) {
    accum |= *buf++ & 0xFF;
    for (i = 0; i < 8; i++) {
      accum <<= 1;
      if (accum & 0x01000000)
        accum ^= 0x00102100;
    }
  }
  // compatibility with XMODEM CRC
  for (j = 0; j < 2; j++) {
    accum |= 0 & 0xFF;
    for (i = 0; i < 8; i++) {
      accum <<= 1;
      if (accum & 0x01000000)
        accum ^= 0x00102100;
    }
  }
  return (accum >> 8);
} // iriCRC

///
// call home
// uses: all.str
// rets: 0=success
int iriDial(void) {
  char str[32];
  int i;
  static char *self="iriDial";
  DBG();
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

