import os, sys
import ProcessItemDialog

from time import time, sleep
from datetime import datetime
from psutil import cpu_count, boot_time, Process as _Process
from collections import namedtuple
from urwid import (
    AttrMap,
    Button,
    Pile,
    Columns,
    Text,
    MainLoop,
    ListBox,
    SimpleListWalker,
    ExitMainLoop,
    connect_signal
)
# reference https://github.com/giampaolo/psutil/blob/88ea5e0b2cc15c37fdeb3e38857f6dab6fd87d12/psutil/_pslinux.py
class Process (AttrMap):
    # Internals
    pid = None
    process = None
    stats = None
    cpu_perc = None

    last_sys_cpu = None
    last_proc_cpu = None

    _timer = getattr(time, 'monotonic', time)

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

    def __init__(self, pid, cb_cursor, cb_remove):
        """
            @method __init__
            @param pid - Process id
            @param cb  - Intended for dynamic updates to parent
            Initializes all internal to the component.
        """
        self.pid = pid
        self.process = p = _Process(pid)

        self.stats = self.read_stat()
        # callbacks to parent
        self.cb_cursor = cb_cursor
        self.cb_remove = cb_remove

        if self.stats is not None:
            self.w_pid = Text(str(pid))
            self.w_name = Text(p.username())
            self.w_pname = Text(self.pget_pname())
            self.w_status = Text('')
            self.w_mem = Text('')
            self.w_cpu = Text('', align='center')
            self.w_uptime = Text('', align='center')
            self.update()

        v = [
            Columns([
                ('fixed', 14, self.w_status),
                ('fixed', 6, self.w_pid),
                self.w_name,
                ('fixed', 8, self.w_cpu),
                ('fixed', 5, self.w_mem),
                ('fixed', 10, self.w_uptime),
                self.w_pname
            ])
        ]
        b = Button('')
        b._w = Pile(v)
        self.popup = ProcessItemDialog.ProcessItemDialog(b, self)
        connect_signal(b, 'click', self.on_click)

        super(Process, self).__init__(self.popup, None, focus_map='reversed')
    def get_pid (self):
        return self.pid
    def on_click (self, item):
        """
            @method on_click
            @param item - Item being interacted with
            connect_signal handler for click event.
            As of now the intended usage is managing the cursor.
        """
        self.item_selected()
        self.cb_cursor(self)
        return True
    def selectable (self):
        """
            @Override urwid.Widget.selectable
            @method selectable
            Makes it so that our item is able to be selected
            from the ListWalker
        """
        return True

    def keypress (self, size, key):
        """
            @Override urwid.Widget
            @method keypress
            @param size - size of the widget taking in the keypress
            @param key  - char repr the key which was pressed
            Handle keypress from context of ProcessListWalker.
            Override intended to determine if the cursor should
            stay at the top, or allow scrolling.
        """
        if key is 'enter':
            self.item_selected()
            return
        self.cb_cursor(key)
        return key

    def item_selected (self):
        """
            Handle the action of selecting an item
        """
        self.popup.open()
    def update (self):
        """
            @method update
            Update method called to redraw the widget
        """
        self.stats = self.read_stat() #if fails, will signal ProcessListWalker to remove
        if self.stats is None:
            return
        p = self.process
        self.cpu_perc = self.pget_cpu()

        self.w_status.set_text(self.pget_status())
        self.w_uptime.set_text(self.pgetf_uptime())
        self.w_mem.set_text("%.1f" % p.memory_percent())
        self.w_cpu.set_text('%.1f' % self.cpu_perc)

    def read_stat (self):
        """
            @method read_stat
            Read /proc/{proc_number}/stat to parse information
            regarding the process.
        """
        f_name = '%s/%s/stat' % ('/proc', self.pid)
        data = None
        try:
            f = open(f_name, 'rb')
            data = f.read()
        except:
            print 'Could not read file: %s' % (f_name)
            self.cb_remove(self)
        if data:
            pat = data.rfind(b')')
            name  = data[data.find(b'(') + 1:pat]
            return [name] + data[pat + 2:].split()
        return None
    def pget_status (self):
        """
            @method pget_status
            Retrieves the status of the proc
        """
        l = self.stats[1]
        return self.PROC_STATS[l]

    def pget_cpu_times (self):
        """
            @method pget_cpu_times
            Returns cpu times in namedtuple
        """

        stats = self.stats
        u_t = float(stats[12]) / self.TICKS # uptime
        u_st = float(stats[13]) / self.TICKS # start
        c_utime = float(stats[14]) / self.TICKS
        c_stime = float(stats[15]) / self.TICKS
        return self.CPUTIMES(u_t, u_st, c_utime, c_stime)

    def pget_cpu (self):
        """
            @method pget_cpu
            Returns cpu alloc of current proc
        """
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

    def pget_pname(self):
        """
            @method pget_pname
            Gets the name of the process
        """
        return self.stats[0]
    def pget_uptime(self):
        """
            @method pget_uptime
            Returns the uptime in sec epoch since boot
        """
        return time() - ((float(self.stats[20]) / self.TICKS) + boot_time())
    def pgetf_uptime(self, f='%H:%M:%S'):
        """
            @method pgetf_uptime
            Return a formatted string repr uptime
        """
        return datetime.fromtimestamp(self.pget_uptime()).strftime(f)
"""
    Testing
"""
if __name__ == '__main__':
    def exit (p):
        if p is 'q':
            raise ExitMainLoop()
    def refresh(loop, data):
        p1.update()
        p2.update()
        loop.set_alarm_in(1, refresh)
    p1 = Process(1, lambda x: x, lambda: x)
    p2 = Process(os.getpid(), lambda x: x, lambda: x)

    lb = ListBox(SimpleListWalker([p1, p2]))

    m = MainLoop(lb, palette=[('reversed', 'standout', ''), ('popbg', 'white', 'dark blue')], pop_ups=True, unhandled_input=exit)
    m.set_alarm_in(1, refresh)
    m.run()
