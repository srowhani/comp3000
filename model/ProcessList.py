import os
import Process

from Component import GenericComponent
from urwid import Columns
PROC_DIR = '/proc'
class ProcessList(GenericComponent):
    process_widgets = dict()
    def __init__ (self):
        self.update()
    def update (self):
        pids = [pid for pid in os.listdir(PROC_DIR) if pid.isdigit()]
        rendered_columns = []
        for pid in pids:
            if pid not in process_widgets:
                process_widgets[pid] = Process(pid)
            rendered_columns.append(process_widgets[pid].update())

        return Columns(render)
