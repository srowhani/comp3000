import os, sys, time
from psutil import cpu_count, Process as _Process
from urwid import Pile, Columns, Text, MainLoop, ListBox, SimpleListWalker, ExitMainLoop
from collections import namedtuple
# reference https://github.com/giampaolo/psutil/blob/88ea5e0b2cc15c37fdeb3e38857f6dab6fd87d12/psutil/_pslinux.py
class Process (Pile):
    # Internals
    pid = None
    process = None
    stats = None
    cpu_perc = None

    last_sys_cpu = None
    last_proc_cpu = None

    _timer = getattr(time, 'monotonic', time.time)

    # Internal widget list
    w_status = None
    w_pid = None
    w_name = None
    w_pname = None
    w_mem = None
    w_cpu = None

    # Constants
    TICKS = os.sysconf("SC_CLK_TCK")

    PROC_STATS = {
        "R": 'running',
        "S": 'sleeping',
        "D": 'disk sleep',
        "T": 'stopped',
        "t": 'tracing stop',
        "Z": 'zombie',
        "X": 'dead',
        "x": 'dead',
        "K": 'wake kill',
        "W": 'waking'
    }
    CPUTIMES = namedtuple('pcputimes', [
        'user',
        'system',
        'children_user',
        'children_system'
    ])
    # Initialize Component
    def __init__(self, pid):
        self.pid = pid
        self.process = p = _Process(pid)

        self.stats = self.read_stat()

        self.w_pid = Text(str(pid))
        self.w_name = Text(p.username())
        self.w_pname = Text(self.pget_name())
        self.w_status = Text('')
        self.w_mem = Text('')
        self.w_cpu = Text('', align='center')


        self.update()

        self.repr = [
            Columns([
                self.w_status,
                self.w_pid,
                self.w_name,
                ('fixed', 5, self.w_mem),
                ('fixed', 8, self.w_cpu),
                self.w_pname
            ])
        ]
        super(Process, self).__init__(self.repr)

    def update (self):
        """ Update method called to redraw the widget """
        p = self.process

        self.stats = self.read_stat()
        self.w_status.set_text(self.pget_status())
        self.w_mem.set_text(str(int(p.memory_percent() * 100)))
        self.cpu_perc = cpu = self.pget_cpu()
        self.w_cpu.set_text('%.1f' % (cpu))

    def read_stat (self):
        """ Read the stat file """
        f_name = '%s/%s/stat' % ('/proc', self.pid)

        try:
            f = open(f_name, 'rb')
            data = f.read()
        except IOError:
            print 'Could not read file: %s' % (f_name)

        if data:
            pat = data.rfind(b')')
            name  = data[data.find(b'(') + 1:pat]
            return [name] + data[pat + 2:].split()

    def pget_status (self):
        """ Retrieves the status of the proc """
        l = self.stats[1]
        return self.PROC_STATS[l]

    def pget_cpu_times (self):
        """ Returns cpu times in namedtuple """

        stats = self.stats
        u_t = float(stats[12]) / self.TICKS # uptime
        u_st = float(stats[13]) / self.TICKS # start
        c_utime = float(stats[14]) / self.TICKS
        c_stime = float(stats[15]) / self.TICKS
        return self.CPUTIMES(u_t, u_st, c_utime, c_stime)

    def pget_cpu (self):
        """ Returns cpu alloc of current proc """
        times = self.pget_cpu_times()
        num_cpus = cpu_count()
        st1 = self.last_sys_cpu
        pt1 = self.last_proc_cpu
        st2 = self._timer() * num_cpus
        pt2 = times
        if st1 is None or pt1 is None:
            self.last_sys_cpu = st2
            self.last_proc_cpu = pt2
            return 0.0
        delta_proc = (pt2.user - pt1.user) + (pt2.system - pt1.system)
        delta_time = st2 - st1
        # reset values for next call in case of interval == None
        self.last_sys_cpu = st2
        self.last_proc_cpu = pt2

        try:
            overall_perc = ((delta_proc / delta_time) * 100)
        except:
            return 0.0
        else:
            perc = overall_perc * (num_cpus or 1)
            return round(perc, 1)

    def pget_name(self):
        """ Gets the name of the process """
        return self.stats[0]
# Testing
if __name__ == '__main__':
    def exit (p):
        """"""
    lb = ListBox(SimpleListWalker([Process(1)]))
    MainLoop(lb, unhandled_input=exit).run()
