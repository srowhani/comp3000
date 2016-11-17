
import time
from urwid import Frame, ProgressBar, AttrMap, ExitMainLoop, MainLoop, ListBox, SimpleListWalker
from Footer import Footer
from Palette import *

class CPUMeter(SimpleListWalker):
	# Internals
	cpu_meter = {}

	def __init__(self):
		"""
			Initializes the widget
		"""
		super(CPUMeter, self).__init__(self)
		self.update()

	def update(self):
		"""
			Calculates cpu percentage
		"""
		c1 = self.readStat()
		time.sleep(0.5)
		c2 = self.readStat()

		# Starts at 1 to skip first cpu
		for i in range(1,len(c1)):
			if 'cpu' in c1[i][0]:
				perc = (int(c1[i][1])+int(c1[i][2])+int(c1[i][3])-                     \
							  int(c2[i][1])-int(c2[i][2])-int(c2[i][3]))/                    \
				       (int(c1[i][1])+int(c1[i][2])+int(c1[i][3])+int(c1[i][4])-       \
							  int(c2[i][1])-int(c2[i][2])-int(c2[i][3])-int(c2[i][4])*1.0)*100
				if i in self.cpu_meter:
					self.cpu_meter[i] = perc
					self[i-1].set_completion(self.cpu_meter[i])
				else:
					self.cpu_meter[i] = perc
					self.append(ProgressBar('body', 'progress', self.cpu_meter[i], 100))  

	def readStat(self):
		"""
			Returns list of CPU info
		"""
		return [i.split() for i in [line.strip() for line in open('/proc/stat')]]


# Testing
if __name__ == '__main__':
	cm = CPUMeter()
	frame = Frame(ListBox(cm), header=None, footer=Footer())

	def exit(key):
		if key in ('q', 'Q'):
			raise ExitMainLoop()

	def refresh(loop, data):
		cm.update()
		loop.set_alarm_in(0.5, refresh)

	main_loop = MainLoop(frame, palette, unhandled_input=exit)
	main_loop.set_alarm_in(0.5, refresh)
	main_loop.run()
