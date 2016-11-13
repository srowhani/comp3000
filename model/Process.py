from Component import GenericComponent
from psutil import Process as _Process
from urwid import Pile, Columns, Text, MainLoop, ListBox, SimpleListWalker, ExitMainLoop

# reference https://github.com/giampaolo/psutil/blob/88ea5e0b2cc15c37fdeb3e38857f6dab6fd87d12/psutil/_pslinux.py
class Process (Pile):
    pid = None
    process = None

    w_status = None
    w_pid = None
    w_name = None
    w_mem = None
    # Initialize Component
    def __init__(self, pid):
        self.pid = pid
        self.process = p = _Process(pid)

        self.w_status = Text(p.status())
        self.w_pid = Text(str(pid))
        self.w_name = Text(p.username())
        self.w_mem = Text(str(int(p.memory_percent() * 100)))

        self.repr = [
            Columns([
                self.w_status,
                self.w_pid,
                self.w_name,
                self.w_mem
            ])
        ]
        super(Process, self).__init__(self.repr)
    # Returns Urwid Widget
    def update (self):
        p = self.process
        self.w_status.set_text(p.status())
        self.w_mem.set_text(str(int(p.memory_percent() * 100)))
# Testing
if __name__ == '__main__':
    def exit (p):
        raise ExitMainLoop()
    lb = ListBox(SimpleListWalker([Process(1)]))
    MainLoop(lb, unhandled_input=exit).run()
