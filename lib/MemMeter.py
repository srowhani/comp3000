
import time
from urwid import (Frame, Button, connect_signal, ProgressBar, 
	AttrMap, ExitMainLoop, MainLoop, ListBox, SimpleListWalker)
from Footer import Footer
from Palette import *

class MemMeter(ProgressBar):

	def __init__(self):
		"""
			Initializes the widget
		"""
		self.mem_perc = 0
		self.total = 0
		self.free = 0
		self.buffers = 0
		self.cached = 0
		super(MemMeter, self).__init__('body', 'progress', self.mem_perc, 100, satt=None)
		self.update()

	def update(self):
		"""
			Calculates mem percentage
		"""
		mem = self.readMemInfo()
		
		# Cygwind doesn't have buffers or cached
		# and vitual box has different locations
		
		for i in range(len(mem)):
			if "MemTotal:" == mem[i][0]:
				self.total = int(mem[i][1])
			if "MemFree:" == mem[i][0]:
				self.free = int(mem[i][1])
			if "Buffers:" == mem[i][0]:
				self.buffers = int(mem[i][1])
			if "Cached:" == mem[i][0]:
				self.cached = int(mem[i][1])
		perc = (self.free+self.buffers+self.cached)/(self.total*1.0)*100
		self.set_completion(perc)

	def readMemInfo(self):
		"""
			Returns list of memory info
		"""
		return [i.split() for i in [line.strip() for line in open('/proc/meminfo')]]

# Testing
if __name__ == '__main__':
	cm = MemMeter()
	frame = Frame(ListBox(SimpleListWalker([cm])), header=None, footer=Footer())

	def exit(key):
		if key in ('q', 'Q'):
			raise ExitMainLoop()

	def refresh(loop, data):
		cm.update()
		loop.set_alarm_in(1, refresh)

	main_loop = MainLoop(frame, palette, unhandled_input=exit, pop_ups=True)
	main_loop.set_alarm_in(1, refresh)
	main_loop.run()
