%module proccoli
%{
%}

extern int send_signal(int pid, int sig);
extern char* read_file(char* fname, int fsize);
