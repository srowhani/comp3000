from Footer import Footer
from Palette import *
from urwid import (
    ExitMainLoop, 
    Frame, 
    ListBox, 
    MainLoop, 
    ProgressBar
)
class MemoryMeter(ProgressBar):

    def __init__(self):
        """
            Initializes the widget
        """
        self.total = 0
        self.free = 0
        self.perc = 0
        super(MemoryMeter, self).__init__('body', 'progress', self.perc, 100, satt=None)
        self.update()

    def update(self):
        """
            Calculates mem percentage
        """
        mem = self.readMemInfo()
        
        # Different index based on Linux version
        for i in range(len(mem)):
            if "MemTotal:" == mem[i][0]:
                self.total = self.toGB(int(mem[i][1]))
            if "MemFree:" == mem[i][0]:
                self.free = self.toGB(int(mem[i][1]))

        try:
            p = 100 - self.free/(self.total*1.0)*100
        except ZeroDivisionError:
            p = 0
        if p < 0: p = 0
        if p > 100: p = 100
        self.perc = p
        self.set_completion(self.perc)

    def getTotal(self):
        return '{:3.3f}'.format(self.total)
    def getUsed(self):
        return '{:3.3f}'.format(self.total - self.free)

    def get_text(self):
        """
            @Override urwid.ProgressBar.get_text()
            Returns the progress bar percentage text
        """
        percent = min(100, max(0, float(self.current * 100 / self.done)))
        return '{:3.1f}'.format(percent) + " %"

    def toGB(self, num):
        """
            Converts kilobytes to gigabytes
        """
        return num/((1024**2)*1.0)

    def readMemInfo(self):
        """
            Returns list of memory info
        """
        return [i.split() for i in [line.strip() for line in open('/proc/meminfo')]]

# Testing
if __name__ == '__main__':
    mm = MemoryMeter()
    frame = Frame(ListBox([mm]), header=None, footer=Footer())

    def exit(key):
        if key in ('q', 'Q'):
            raise ExitMainLoop()

    def refresh(loop, data):
        mm.update()
        loop.set_alarm_in(1, refresh)

    main_loop = MainLoop(frame, palette, unhandled_input=exit, pop_ups=True)
    main_loop.set_alarm_in(1, refresh)
    main_loop.run()
