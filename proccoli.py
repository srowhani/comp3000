#
# Contributors
# 	Shane Slatter 100946497
# 	Seena Rowhani 100945353
#
# Description
# 	A process manager written in python
#

import urwid
import psutil

from random import randint

processes = [psutil.Process(i) for i in psutil.pids()]

def exit(key):
	if key in ('q', 'Q'):
		raise urwid.ExitMainLoop()

def main():
	text_tasks = [
		"Tasks:  ",
		str(len(processes)), " total,   ",
		str(len([i for i in processes if i.status() is 'running'])), " running,   ",
		str(len([i for i in processes if i.status() is 'waiting'])), " waiting,   ",
		str(len([i for i in processes if i.status() is 'stopped'])), " stopped,   ",
		str(len([i for i in processes if i.status() is 'zombie'])),  " zombie",
	]

	progress = [urwid.ProgressBar('body', 'progress', i, 100)
		for i in psutil.cpu_percent(interval=1, percpu=True)]

	cpuColumns = [urwid.Columns([
		('fixed', 10, urwid.Text("CPU-{}%: ".format(i), align='left')),
		('fixed', 3, urwid.Text(" [", align='right')),
		('weight', 1, progress[i]),
		('fixed', 3, urwid.Text(" ]", align='left')),
		# add more
		], 0, min_width=8) for i in range(0, len(progress))]

	blank = urwid.Divider()

	listbox_content = [
		blank,
		urwid.Pile(cpuColumns),
		blank,
		urwid.AttrWrap(urwid.Columns([
			('fixed', 10, urwid.Text("STATUS", align='right')),
			('fixed', 10, urwid.Text("PID",  align='right')),
			('fixed', 15, urwid.Text("USER", align='right')),
			('fixed', 10, urwid.Text("MEM %", align='right')),
			# add more
			], 0, min_width=8), 'header'),
		urwid.Columns([
			('fixed', 10, urwid.Text([str(i.status()) + "\n" for i in processes],  align='right')),
			('fixed', 10, urwid.Text([str(i.pid) + "\n" for i in processes],  align='right')),
			('fixed', 15, urwid.Text([i.username() + "\n" for i in processes], align='right')),
			('fixed', 10, urwid.Text([str(int(i.memory_percent() * 100)) + "%\n" for i in processes], align='right')),
			# add more
			], 0, min_width=8),
		blank
	]


	header = urwid.AttrWrap(urwid.Text(text_tasks), 'header')
	listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
	frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)

	palette = [
		('header', 'white', 'dark red', 'bold'),
		('progress', 'white', 'light blue', 'bold'),
		('body', 'black', 'light gray', 'standout'),
	]

	def refresh(loop, data):
		cpu_percentages = psutil.cpu_percent(interval=1, percpu=True)
		for i in range(0, len(cpu_percentages)):
			progress[i].set_completion(cpu_percentages[i])
		c = urwid.Columns([
			('fixed', 10, urwid.Text([str(i.status()) + "\n" for i in processes],  align='right')),
			('fixed', 10, urwid.Text([str(i.pid) + "\n" for i in processes],  align='right')),
			('fixed', 15, urwid.Text([i.username() + "\n" for i in processes], align='right')),
			('fixed', 10, urwid.Text([str(int(i.memory_percent() * 100)) + "%\n" for i in processes], align='right')),
			# add more
		], 0, min_width=8)

		listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))

		loop.set_alarm_in(2, refresh)


	mainloop = urwid.MainLoop(frame, palette, unhandled_input=exit)
	mainloop.set_alarm_in(2, refresh)
	mainloop.run()


if __name__=='__main__':
	main()
