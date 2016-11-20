
import time
from urwid import ProgressBar, AttrWrap, ExitMainLoop, MainLoop, ListBox, SimpleListWalker
from Palette import *

class CPUMeter(SimpleListWalker):
	cpu_meter = {}

	def __init__(self):
		super(CPUMeter, self).__init__(self)
		self.update()

	def update(self):
		c1 = [i.split() for i in [line.strip() for line in open('/proc/stat')]]
		time.sleep(0.5)
		c2 = [i.split() for i in [line.strip() for line in open('/proc/stat')]]

		# Starts at 1 to skip first cpu
		for i in range(1,len(c1)):
			if 'cpu' in c1[i][0]:
				top = int(c1[i][1])+int(c1[i][2])+int(c1[i][3])- \
							int(c2[i][1])-int(c2[i][2])-int(c2[i][3])
				btm = int(c1[i][1])+int(c1[i][2])+int(c1[i][3])+int(c1[i][4])- \
							int(c2[i][1])-int(c2[i][2])-int(c2[i][3])-int(c2[i][4])*1.0
				if i in self.cpu_meter:
					self.cpu_meter[i] = (top/btm*100)
					self[i-1].set_completion(self.cpu_meter[i])
				else:
					self.cpu_meter[i] = (top/btm*100)
					self.append(ProgressBar('body', 'progress', self.cpu_meter[i], 100))	

# Testing
if __name__ == '__main__':
	
	cm = CPUMeter()
	lb = ListBox(cm)

	def exit(key):
		if key in ('q', 'Q'):
			raise ExitMainLoop()

	def refresh(loop, data):
		cm.update()
		loop.set_alarm_in(0.5, refresh)

	main_loop = MainLoop(lb, palette, unhandled_input=exit)
	main_loop.set_alarm_in(0.5, refresh)
	main_loop.run()
