#include <stdio.h>
#include <string.h>

// required for pin related issue
char *strcpy_wrapper(char *dst, char *src) {
  return strcpy(dst, src);
}

int main(int argc, char ** argv) {
  char buf[10];

  if (argc < 2)
    return -1;

  printf(argv[1]);

  strcpy_wrapper(buf, argv[1]);

  return 0;
}
