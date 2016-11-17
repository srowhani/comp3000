
from urwid import Columns, Frame, Text, ListBox, ExitMainLoop, MainLoop
from CPUMeter import CPUMeter
from Footer import Footer
from Palette import *

class CPUList(ListBox):
	# Internals 
	cpu_text = {}
	cpu_columns = {}
	cpu_meter = None

	def __init__(self):
		"""
				Initializes the widgets
		"""
		self.cpu_meter = CPUMeter()
		super(CPUList, self).__init__(self.cpu_columns)
		self.update()

	def update(self):
		"""
				Stores all CPU widgets
				Updates child component
		"""
		stat = self.cpu_meter.readStat()

		# Starts at 1 to skip first cpu
		for i in range(1,len(stat)):
			if 'cpu' in stat[i][0]:
				self.cpu_text[i] = stat[i][0]

		for i in range(len(self.cpu_text)):
			self.cpu_columns[i] = Columns([
				('fixed',  5, Text("%"+self.cpu_text[i+1], align='left')),
				('fixed',  3, Text(" [", align='right')),
				('weight', 1, self.cpu_meter[i]),
				('fixed',  3, Text("] ", align='left')),
				])

		self.cpu_meter.update()

# Testing
if __name__ == '__main__':
	lb = CPUList()
	frame = Frame(lb, header=None, footer=Footer())

	def exit(key):
		if key in ('q', 'Q'):
			raise ExitMainLoop()

	def refresh(loop, data):
		lb.update()
		loop.set_alarm_in(1, refresh)

	main_loop = MainLoop(frame, palette, unhandled_input=exit)
	main_loop.set_alarm_in(1, refresh)
	main_loop.run()
