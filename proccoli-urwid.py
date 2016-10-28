#
# Contributors
# 	Shane Slatter 100946497
# 	Seena Rowhani 100945353
#
# Description
# 	A process manager written in python
#

import urwid
from random import randint

running = 1
waiting = 2
stopped = 3
zombie  = 4

pid  = ['100\n', '101\n', '102\n',]
user = ['Shane\n', 'Shane\n', 'Shane\n',]
pr   = ['8\n', '8\n', '8\n']

cpu = []
for i in range(0, 4):
	cpu.append('%CPU{} :   '.format(i))

rand = [randint(0, 100) for p in range(0,4)]

def exit(key):
	if key in ('q', 'Q'):
		raise urwid.ExitMainLoop()

def main():

	text_tasks = [
		"Tasks:  ", 
		str(running+waiting+stopped+zombie), " total,   ", 
		str(running), " running,   ",
		str(waiting), " waiting,   ",
		str(stopped), " stopped,   ",
		str(zombie),  " zombie",
		]

	progress = [urwid.ProgressBar('body', 'progress', rand[i], 100) 
		for i in range(0,4)]

	cpuColumns = [urwid.Columns([
		('fixed', 10, urwid.Text(cpu[i], align='left')),
		('fixed', 3, urwid.Text(" [", align='right')),
		('weight', 1, progress[i]),
		('fixed', 3, urwid.Text(" ]", align='left')),
		# add more
		], 0, min_width=8) for i in range(0, 4)]

	blank = urwid.Divider()

	listbox_content = [
		blank,
		urwid.Pile([cpuColumns[i] for i in range(0, 4)]),
		blank,
		urwid.AttrWrap(urwid.Columns([
			('fixed', 9, urwid.Text("PID",  align='right')),
			('fixed', 9, urwid.Text("USER", align='right')),
			('fixed', 6, urwid.Text("PR",   align='right')),
			# add more
			], 0, min_width=8), 'header'),
		urwid.Columns([
			('fixed', 9, urwid.Text(pid,  align='right')),
			('fixed', 9, urwid.Text(user, align='right')),
			('fixed', 6, urwid.Text(pr, align='right')),
			# add more
			], 0, min_width=8),
		blank,
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
		r = [randint(0, 100) for p in range(0,4)]
		for i in range(0,4):
			progress[i].set_completion(r[i])
		loop.set_alarm_in(2, refresh)

	mainloop = urwid.MainLoop(frame, palette, unhandled_input=exit)
	mainloop.set_alarm_in(2, refresh)
	mainloop.run()


if __name__=='__main__':
	main()

