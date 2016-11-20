#include <signal.h>

#include <stdio.h>
#include <stdlib.h>

int send_signal(int pid, int sig)
{
  return kill(pid, sig);
}

char* read_file (const char* filename, int fsize)
{
  FILE *f = fopen(filename, "rb");
  char *string = malloc(fsize + 1);
  fread(string, fsize, 1, f);
  fclose(f);
  string[fsize] = 0;
  return string;
}
