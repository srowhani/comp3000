%module proccoli
%{
/* Put header files here or function declarations like below */
extern int proccoli_sig(int pid, int sig);
%}

extern int proccoli_sig(int pid, int sig);
