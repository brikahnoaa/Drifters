#include <stdio.h>
#include <stdlib.h>

unsigned int iriCRC(unsigned char *buf, int cnt) {
  long accum=0x00000000;
  int i, j;
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

int main() {
  char *buff;
  unsigned int cs;
  FILE *fd;
  int cnt, len;
  //
  buff=malloc(64);
  // platform
  len = 8;
  sprintf(buff, "???CS%4s%4s", "LR01", "QUEH");
  cs = iriCRC(buff+5, len);
  buff[3] = (char) (cs >> 8) & 0xFF;
  buff[4] = (char) (cs & 0xFF);
  printf("\n crc %x %u \n", cs, cs);
  fd = fopen("platform.hdr", "w");
  fwrite(buff, sizeof(char), len+5, fd);
  fclose(fd);
  // message
  len = 10;
  sprintf(buff, "@@@CS%c%cT%c%c%5s", 
      (char) (len>>8 & 0xFF), (char) (len & 0xFF),
      1, 1, "Hello");
  cs = iriCRC(buff+5, len);
  buff[3] = (char) (cs >> 8) & 0xFF;
  buff[4] = (char) (cs & 0xFF);
  printf("\n crc %x %u \n", cs, cs);
  fd = fopen("message.blk", "w");
  fwrite(buff, sizeof(char), len+5, fd);
  fclose(fd);
}
