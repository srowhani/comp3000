
from urwid import Padding, Filler, LineBox, AttrMap, Button, Pile, Columns, Frame, Text, ListBox, ExitMainLoop, MainLoop
from CPUMeter import CPUMeter
from Footer import Footer
from Palette import *

class CPUList(ListBox):
	# Internals 
	cpu_text = {}
	cpu_columns = {}

	def __init__(self):
		"""
			Initializes the widgets
		"""
		self.stat = self.getStat()
		self.cpu_meter = CPUMeter()
		self.CpuColumns()
		super(CPUList, self).__init__(self.cpu_columns)
		self.update()

	def CpuColumns(self):
		# Starts at 1 to skip first cpu (total cpu)
		for i in range(1,len(self.stat)):
			if 'cpu' in self.stat[i][0]:
				self.cpu_text[i] = self.stat[i][0]

		for i in range(len(self.cpu_text)):
			self.cpu_columns[i] = Columns([
				('fixed',  5, Text("%"+self.cpu_text[i+1], align='left')),
				('fixed',  3, Text(" [", align='right')),
				('weight', 1, self.cpu_meter[i]),
				('fixed',  3, Text("] ", align='left')),
				])

	def update(self):
		"""
			Updates child component
		"""
		self.cpu_meter.update()

	def getStat(self):
		return [i.split() for i in [line.strip() for line in open('/proc/stat')]]

# Testing
if __name__ == '__main__':
	cpu_lb = CPUList()
	lb = Padding(cpu_lb, left=2, right=2)

	footer = Footer()
	frame = Frame(lb, footer=footer)

	def keyPress(key):
		if key in ('q', 'Q'):
			raise ExitMainLoop()

	def refresh(loop, data):
		cpu_lb.update()
		loop.set_alarm_in(1, refresh)

	main_loop = MainLoop(frame, palette, unhandled_input=keyPress, pop_ups=True)
	main_loop.set_alarm_in(1, refresh)
	main_loop.run()
