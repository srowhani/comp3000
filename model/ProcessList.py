import os
from Process import Process

from Component import GenericComponent
from urwid import Columns, ListBox, SimpleListWalker, MainLoop, ExitMainLoop
PROC_DIR = '/proc'
class ProcessList(GenericComponent):
    process_widgets = dict()
    def __init__ (self):
        self.update()

    def update (self):
        pids = [pid for pid in os.listdir(PROC_DIR) if pid.isdigit()]
        rendered_columns = []
        for pid in pids:
            if pid not in self.process_widgets:
                self.process_widgets[pid] = Process(int(pid))
            rendered_columns.append(self.process_widgets[pid].update())
        return ListBox(SimpleListWalker(rendered_columns))

# Testing
if __name__ == '__main__':
    pl = ProcessList()
    test_processes = pl.update()

    def exit (p):
        raise ExitMainLoop()
    def refresh(loop, data):
        test_procceses = pl.update()
        loop.set_alarm_in(2, refresh)

    main_loop = MainLoop(test_processes, unhandled_input=exit)
    main_loop.set_alarm_in(2, refresh)

    main_loop.run()
