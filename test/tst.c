#include <stdio.h>
#include <stdlib.h>
#include <string.h>


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
    printf("accum %u\n", accum);
  }
  // compatibility with XMODEM CRC
  for (j = 0; j < 2; j++) {
    // accum |= 0 & 0xFF;
    for (i = 0; i < 8; i++) {
      accum <<= 1;
      if (accum & 0x01000000)
        accum ^= 0x00102100;
    }
    printf("accum %u\n", accum);
  }
  return (accum >> 8);
} // iriCRC

int main() {
    char *str;
    unsigned int cs;
    str = "abc";
    str = "a";
    cs = iriCRC(str, strlen(str));
    printf("str %s cs %x %u\n", str, cs, cs);

}
