#include <signal.h>
#include <errno.h>
#include <string.h>

int proccoli_sig(int pid, int sig) {
  return kill(pid, sig);
}
