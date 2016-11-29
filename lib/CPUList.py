
from urwid import (Padding, Filler, LineBox, AttrMap, Button, 
	Pile, Columns, Frame, Text, ListBox, ExitMainLoop, MainLoop)
from CPUMeter import CPUMeter
from MemoryMeter import MemoryMeter
from SwapMeter import SwapMeter
from Footer import Footer
from Palette import *

class CPUList(ListBox):
	# Internals 
	cpu_text = {}
	cpu_columns = {}

	m_perc = Text("", align='right')
	m_total = Text("", align='left')
	s_perc = Text("", align='right')
	s_total = Text("", align='left')

	def __init__(self):
		"""
			Initializes the widgets
		"""
		self.stat = self.readStat()
		self.cpu_meter = CPUMeter()
		self.mem_meter = MemoryMeter()
		self.swap_meter = SwapMeter()
		self.Columns()
		super(CPUList, self).__init__(self.cpu_columns)
		self.update()

	def Columns(self):
		# Starts at 1 to skip first cpu (total cpu)
		for i in range(1,len(self.stat)):
			if 'cpu' in self.stat[i][0]:
				self.cpu_text[i] = self.stat[i][0]

		for i in range(len(self.cpu_text)):
			self.cpu_columns[i] = Columns([
				('fixed',  7, Text("%"+self.cpu_text[i+1]+":", align='left')),
				('fixed', 12, Text("")),
				('fixed',  2, Text(" [")),
				('weight', 1, self.cpu_meter[i]),
				('fixed',  2, Text("] ")),
				])
		self.cpu_columns[len(self.cpu_columns)] = Columns([
			('fixed',  7, Text("Mem:")),
			('fixed',  5, self.m_perc),
			('fixed',  1, Text("/")),
			('fixed',  7, self.m_total),
			('fixed',  1, Text("[")),
			('weight', 1, self.mem_meter),
			('fixed',  2, Text("] ")),
			])
		self.cpu_columns[len(self.cpu_columns)] = Columns([
			('fixed',  7, Text("Swap:")),
			('fixed',  5, self.s_perc),
			('fixed',  1, Text("/")),
			('fixed',  7, self.s_total),
			('fixed',  1, Text("[")),
			('weight', 1, self.swap_meter),
			('fixed',  2, Text("] ")),
			])


	def update(self):
		"""
			Updates child components
		"""
		self.s_perc.set_text(self.swap_meter.getPerc())
		self.s_total.set_text(self.swap_meter.getTotal())
		self.m_perc.set_text(self.mem_meter.getPerc())
		self.m_total.set_text(self.mem_meter.getTotal())
		self.mem_meter.update()
		self.cpu_meter.update()
		self.swap_meter.update()

	def readStat(self):
		"""
			Returns list of CPU info
		"""
		return [i.split() for i in [line.strip() for line in open('/proc/stat')]]

# Testing
if __name__ == '__main__':
	cpu_lb = CPUList()
	lb = cpu_lb

	frame = Frame(lb, header=None, footer=Footer())

	def keyPress(key):
		if key in ('q', 'Q'):
			raise ExitMainLoop()

	def refresh(loop, data):
		cpu_lb.update()
		loop.set_alarm_in(1.5, refresh)

	main_loop = MainLoop(frame, palette, unhandled_input=keyPress, pop_ups=True)
	main_loop.set_alarm_in(1.5, refresh)
	main_loop.run()
