#
# Contributors
# 	Shane Slatter 100946497
# 	Seena Rowhani 100945353
#
# Description
# 	A process manager written in python
#

from urwid import (
	Frame,
	BoxAdapter,
	MainLoop,
	ExitMainLoop
)

from lib.ResourceManager import ResourceManager
from lib.ProcessTable import ProcessTable
from lib.Footer import Footer
from lib.Palette import palette

def main():
	# optional param # rows
	p = ProcessTable()
	r = ResourceManager()
	# height is num_cpus rows + mem row + swap row + empty row
	r_height = len(r.cpu_meters) + 3
	frame = Frame(p, header=BoxAdapter(r, r_height), footer=Footer())

	def exit(key):
		if key in ('q', 'Q'):
			raise ExitMainLoop()
	def refresh(loop, data):
		p.update()
		r.update()
		loop.set_alarm_in(2, refresh)

	mainloop = MainLoop(frame, palette, pop_ups=True, unhandled_input=exit)
        mainloop.set_alarm_in(0, refresh)
	mainloop.run()

if __name__=='__main__':
	main()
