#include <stdio.h>
#include <string.h>

/* for pin too bug */
char *strncpy_wrapper(char *dst, char *src, size_t n)
{
    return strncpy(dst, src, n);
}

int main() {
    char *s = "TAINTED";       // 0x400694
    char buf[20];
    int i = 0;
    while(s[i] != '\0') i++;
    strncpy_wrapper(buf, s, i);
    return 0;
}
