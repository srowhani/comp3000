import os

from Process import Process

from urwid import ListBox, SimpleFocusListWalker, MainLoop, ExitMainLoop, connect_signal

PROC_DIR = '/proc'

class ProcessListWalker(SimpleFocusListWalker):
    process_dict = {} # check if process already exists in O(1)
    process_list = []
    
    at_top = True
    sort_var = 'cpu_perc'
    asc=True
    def __init__ (self):
        """
            @method __init__
            Initializes the widgets
        """
        super(ProcessListWalker, self).__init__(self.process_list)
        self.update()
        print self.focus
    def update (self):
        """
            @method update
            Finds new processes by use of memoization
            Iteratively updates or creates an entry for
            processes
        """
        pids = [int(pid) for pid in os.listdir(PROC_DIR) if pid.isdigit()]
        for pid in pids:
            if pid in self.process_dict: # it already exists
                self.process_dict[pid].update()
            else:
                p = Process(pid, self.item_focus)
                self.process_dict[pid] = p
                self.append(p)
        self.sort(key = lambda x: getattr(x, self.sort_var), reverse=self.asc)
        if self.at_top:
            self.set_focus(0)
        # print self.focus
    def item_focus (self, obj):
        """
            @method item_focus
            @param obj
                Either
                    an instance of a Process
                    letter repr a keypress

            Maintains at_top, by parsing actions
            propogated up from the individual processes.
        """
        if isinstance(obj, Process):
            self.at_top = self.index(obj) is 0
            return
        key = obj
        if key is 'up':
            self.at_top = self.focus is 0
        elif key is 'down':
            self.at_top = False

"""
    Testing
"""
if __name__ == '__main__':
    pl = ProcessListWalker()
    lb = ListBox(pl)
    def exit (p):
        if p is 'q':
            raise ExitMainLoop()
    def refresh(loop, data):
        pl.update()
        loop.set_alarm_in(1, refresh)

    main_loop = MainLoop(lb, unhandled_input=exit)
    main_loop.set_alarm_in(1, refresh)

    main_loop.run()
