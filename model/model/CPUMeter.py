
from urwid import ProgressBar, AttrWrap, ExitMainLoop, MainLoop, ListBox, SimpleListWalker
from time import sleep
from Palette import *

class CPUMeter():

	def __init__ (self):
		self.update()

	def update (self):
		cpu_meter = []

		cpu1 = [i.split() for i in [line.strip() for line in open('/proc/stat')]]
		sleep(0.8)
		cpu2 = [i.split() for i in [line.strip() for line in open('/proc/stat')]]

		# Calculate cpu percentage /100
		for i in range(1,len(cpu1)):
			if 'cpu' in cpu1[i][0]:
				top = int(cpu1[i][1])+int(cpu1[i][2])+int(cpu1[i][3])- \
							int(cpu2[i][1])-int(cpu2[i][2])-int(cpu2[i][3])
				btm = int(cpu1[i][1])+int(cpu1[i][2])+int(cpu1[i][3])+int(cpu1[i][4])- \
							int(cpu2[i][1])-int(cpu2[i][2])-int(cpu2[i][3])-int(cpu2[i][4])*1.0
				cpu_meter.append((top/btm*100))

		# Testing
		#print cpu_meter[0]

		progress = [ProgressBar('body', 'progress', cpu_meter[i], 100) for i in range(len(cpu_meter))]

		for i in range(len(progress)):
			progress[i].set_completion(cpu_meter[i])

		return progress
		#return AttrWrap(ListBox(SimpleListWalker(progress)), 'body')

if __name__ == '__main__':
	
	test = CPUMeter().update()

	def exit(key):
		if key in ('q', 'Q'):
			raise ExitMainLoop()

	def refresh(loop, data):
		test = CPUMeter().update()
		loop.set_alarm_in(1, refresh)

	main_loop = MainLoop(test, palette, unhandled_input=exit)
	main_loop.set_alarm_in(1, refresh)
	main_loop.run()
