from Component import GenericComponent
from psutil import Process as _Process
from urwid import Pile, Columns, Text
PROC_DIR = '/proc'
# reference https://github.com/giampaolo/psutil/blob/88ea5e0b2cc15c37fdeb3e38857f6dab6fd87d12/psutil/_pslinux.py
class Process (GenericComponent):
    pid = None
    process = None
    # Initialize Component
    def __init__(self, pid):
        self.update()
        self.pid = pid
        self.process = _Process(pid)

    # Returns Urwid Widget
    def update (self):
        p = self.process
        return Pile([
            Text(('bold', p.status())),
            Text(('bold', str(p.pid))),
            Text(('bold', p.username())),
            Text(('bold', str(int(p.memory_percent() * 100)) + "%\n"))
        ])
