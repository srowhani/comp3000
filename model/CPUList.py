
from urwid import Columns, AttrWrap, Text, SimpleListWalker, ListBox, ExitMainLoop, MainLoop
from time import sleep
from CPUMeter import CPUMeter
from Palette import *

class CPUList ():

	def __init__ (self):
		self.update()

	def update (self):
		cpu = []

		stat = [i.split() for i in [line.strip() for line in open('/proc/stat')]]

		for i in range(1,len(stat)):
			if 'cpu' in stat[i][0]:
				cpu.append(stat[i][0])

		cpu_meter = CPUMeter().update()

		cpuColumns = [Columns([
			('fixed',  8, Text(cpu[i], align='left')),
			('fixed',  3, Text(" [", align='right')),
			('weight', 1, cpu_meter[i]),
			('fixed',  3, Text(" ]", align='left')),
			], 0, min_width=8) for i in range(len(cpu))]

		#return cpuColumns
		return AttrWrap(ListBox(SimpleListWalker(cpuColumns)), 'body')


if __name__ == '__main__':

	test = AttrWrap(CPUList().update(), 'body')

	def exit(key):
		if key in ('q', 'Q'):
			raise ExitMainLoop()

	def refresh(loop, data):
		test = AttrWrap(CPUList().update(), 'body')
		loop.set_alarm_in(1, refresh)

	main_loop = MainLoop(test, palette, unhandled_input=exit)
	main_loop.set_alarm_in(1, refresh)
	main_loop.run()
