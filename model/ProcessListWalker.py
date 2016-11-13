import os

from Process import Process

from urwid import ListBox, SimpleListWalker, MainLoop, ExitMainLoop

PROC_DIR = '/proc'

class ProcessListWalker(SimpleListWalker):
    process_dict = {} # check if process already exists in O(1)

    def __init__ (self):
        super(ProcessListWalker, self).__init__([])
        self.update()

    def update (self):
        pids = [int(pid) for pid in os.listdir(PROC_DIR) if pid.isdigit()]
        for pid in pids:
            if pid in self.process_dict: # it already exists
                self.process_dict[pid].update()
            else:
                p = Process(pid)
                self.process_dict[pid] = p
                self.append(p)

# Testing
if __name__ == '__main__':
    pl = ProcessListWalker()
    lb = ListBox(pl)
    def exit (p):
        raise ExitMainLoop()
    def refresh(loop, data):
        pl.update()
        loop.set_alarm_in(1, refresh)

    main_loop = MainLoop(lb, unhandled_input=exit)
    main_loop.set_alarm_in(1, refresh)

    main_loop.run()
