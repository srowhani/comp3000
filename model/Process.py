from Component import GenericComponent
from psutil import Process as _Process
from urwid import Pile, Columns, Text, MainLoop, ListBox, SimpleListWalker, ExitMainLoop

# reference https://github.com/giampaolo/psutil/blob/88ea5e0b2cc15c37fdeb3e38857f6dab6fd87d12/psutil/_pslinux.py
class Process (GenericComponent):
    pid = None
    process = None
    # Initialize Component
    def __init__(self, pid):
        self.pid = pid
        self.process = _Process(pid)

    # Returns Urwid Widget
    def update (self):
        p = self.process
        pid = str(self.pid)
        status = p.status()
        mem = str(int(p.memory_percent() * 100))
        name = p.username()

        return Pile([
            Columns([
                ('fixed', 10, Text(status, align='left')),
                ('fixed', 10, Text(pid)),
                ('fixed', 10, Text(name)),
                ('fixed', 10, Text(mem, align='right'))
            ])
        ])
# Testing
if __name__ == '__main__':
    def exit (p):
        raise ExitMainLoop()
    test_process = Process(1).update()
    lb = ListBox(SimpleListWalker([test_process]))
    MainLoop(lb, unhandled_input=exit).run()
