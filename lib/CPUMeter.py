from Footer import Footer
from Palette import *
from urwid import (
    ExitMainLoop, 
    Frame, 
    ListBox, 
    MainLoop, 
    ProgressBar
)

class CPUMeter(ProgressBar):

    def __init__(self, index):
        """
            Initializes the widget
        """
        self.index = index
        self.stat = self.readStat()
        self.system = 0
        self.niced = 0
        super(CPUMeter, self).__init__('body', 'progress', 0, 100, satt=None)
        self.update()

    def update(self):
        """
            Calculates cpu percentage
        """
        old = self.stat
        new = self.readStat()
        perc = self.calcPerc(self.index, old, new)
        self.system = self.calcSystem(self.index, old, new)
        self.niced = self.calcNiced(self.index, old, new)
        self.set_completion(perc)
        self.stat = self.readStat()

    def getSystem(self):
        return '{:3.2f}'.format(abs(self.system))
    def getNiced(self):
        return '{:3.2f}'.format(abs(self.niced))

    def calcPerc(self, i, a, b):
        """
            Calculates the total cpu percentage
        """
        try:
          p = (int(a[i][1])+int(a[i][2])+int(a[i][3])-                    \
                     int(b[i][1])-int(b[i][2])-int(b[i][3]))/                   \
                    (int(a[i][1])+int(a[i][2])+int(a[i][3])+int(a[i][4])-       \
                     int(b[i][1])-int(b[i][2])-int(b[i][3])-int(b[i][4])*1.0)*100
        except ZeroDivisionError:
            p = 0
        if p < 0: p = 0
        if p > 100: p = 100
        return p

    def calcNiced(self, i, a, b):
        """
            Calculates the combined un-niced and niced user processes percentage
        """
        try:
          p = (int(a[i][1])+int(a[i][2])-                    \
                     int(b[i][1])-int(b[i][2]))/                   \
                    (int(a[i][1])+int(a[i][2])+int(a[i][4])-       \
                     int(b[i][1])-int(b[i][2])-int(b[i][4])*1.0)*100
        except ZeroDivisionError:
            p = 0
        if p < 0: p = 0
        if p > 100: p = 100
        return p

    def calcSystem(self, i, a, b):
        """
            Calculates the runnning kernel process percentage
        """
        try:
          p = (int(a[i][3])-                    \
                     int(b[i][3]))/                   \
                    (int(a[i][3])+int(a[i][4])-       \
                     int(b[i][3])-int(b[i][4])*1.0)*100
        except ZeroDivisionError:
            p = 0
        if p < 0: p = 0
        if p > 100: p = 100
        return p

    def get_text(self):
        """
            @Override urwid.ProgressBar.get_text()
            Returns the progress bar percentage text
        """
        percent = min(100, max(0, float(self.current * 100 / self.done)))
        return '{:3.1f}'.format(percent) + " %"

    def readStat(self):
        """
            Returns list of CPU info
        """
        return [i.split() for i in [line.strip() for line in open('/proc/stat')]]

# Testing
if __name__ == '__main__':
    cm = CPUMeter(1) 
    frame = Frame(ListBox([cm]), header=None, footer=Footer())

    def exit(key):
        if key in ('q', 'Q'):
            raise ExitMainLoop()

    def refresh(loop, data):
        cm.update()
        loop.set_alarm_in(1, refresh)

    main_loop = MainLoop(frame, palette, unhandled_input=exit, pop_ups=True)
    main_loop.set_alarm_in(1, refresh)
    main_loop.run()
