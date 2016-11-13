
import urwid
from time import sleep
from math import ceil
from Component import GenericComponent
from CPUMeter import CPUMeter

class CPUList (GenericComponent):

	def __init__ (self):
		self.update()

	def update (self):
		cpu = []

		stat = [i.split() for i in [line.strip() for line in open('/proc/stat')]]

		for i in range(1,len(stat)):
			if 'cpu' in stat[i][0]:
				cpu.append(stat[i][0])

		meter = CPUMeter().update()

		cpuColumns = [urwid.Columns([
			('fixed', 8, urwid.Text(cpu[i], align='left')),
			('fixed',  3, urwid.Text(" [", align='right')),
			('weight', 1, meter[i]),
			('fixed',  3, urwid.Text(" ]", align='left')),
			], 0, min_width=8) for i in range(len(cpu))]

		#return cpuColumns
		return urwid.ListBox(urwid.SimpleListWalker(cpuColumns))

if __name__ == '__main__':

	test = CPUList().update()

	def exit(key):
		if key in ('q', 'Q'):
			raise urwid.ExitMainLoop()

	def refresh(loop, data):
		test = CPUList().update()
		loop.set_alarm_in(2, refresh)

	main_loop = urwid.MainLoop(test, unhandled_input=exit)
	main_loop.set_alarm_in(2, refresh)
	main_loop.run()
