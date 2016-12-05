from CPUMeter import CPUMeter
from Footer import Footer
from Palette import *
from urwid import (
    ExitMainLoop,
    Frame,
    ListBox,
    MainLoop,
    SimpleListWalker
)

class CPUListWalker(SimpleListWalker):
    # Internals
    cpu_meter = {}

    def __init__(self):
        """
            Initializes the widget
        """
        self.stat = self.readStat()
        super(CPUListWalker, self).__init__(self)
        self.update()

    def update(self):
        """
            Creates and updates child widgets
        """
        # Starts at 1 to skip first cpu (total cpu)
        for i in range(1,len(self.stat)):
            if 'cpu' in self.stat[i][0]:
                if i in self.cpu_meter:
                    self.cpu_meter[i].update()
                else:
                    self.cpu_meter[i] = CPUMeter(i)
                    self.append(self.cpu_meter[i])

    def readStat(self):
        """
            Returns list of CPU info
        """
        return [i.split() for i in [line.strip() for line in open('/proc/stat')]]

# Testing
if __name__ == '__main__':
    cm = CPUListWalker()
    frame = Frame(ListBox(cm), header=None, footer=Footer())

    def exit(key):
        if key in ('q', 'Q'):
            raise ExitMainLoop()

    def refresh(loop, data):
        cm.update()
        loop.set_alarm_in(1, refresh)

    main_loop = MainLoop(frame, palette, unhandled_input=exit, pop_ups=True)
    main_loop.set_alarm_in(1, refresh)
    main_loop.run()
