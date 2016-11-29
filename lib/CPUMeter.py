
from urwid import (Frame, Button, Columns, Text, ProgressBar, 
	AttrMap, ExitMainLoop, MainLoop, ListBox, SimpleListWalker)
from Footer import Footer
from Palette import *

class CPUMeter(SimpleListWalker):
	# Internals
	cpu_meter = {}

	def __init__(self):
		"""
			Initializes the widget
		"""
		self.stat = self.readStat()
		super(CPUMeter, self).__init__(self)
		self.update()

	def update(self):
		"""
			Calculates cpu percentage
		"""
		old = self.stat
		new = self.readStat()

		# Starts at 1 to skip first cpu (total cpu)
		for i in range(1,len(self.stat)):
			if 'cpu' in old[i][0]:
				perc = self.calcPerc(i, old, new)
				if i in self.cpu_meter:
					self.cpu_meter[i] = perc
					self[i-1].set_completion(self.cpu_meter[i])
				else:
					self.cpu_meter[i] = perc
					self.append(ProgressBar('body', 'progress', self.cpu_meter[i], 100, None))
					
		self.stat = self.readStat()

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
		loop.set_alarm_in(1, refresh)

	main_loop = MainLoop(frame, palette, unhandled_input=exit, pop_ups=True)
	main_loop.set_alarm_in(1, refresh)
	main_loop.run()
