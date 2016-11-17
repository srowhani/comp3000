
from urwid import AttrMap, Text, ExitMainLoop, MainLoop, Frame, ListBox, SimpleListWalker
from Palette import *

class Footer(AttrMap):
	# Constants
	footer_text = [
		" ",
		('key', "q/Q"), " quit   ",
		('key', "F1"), " filter   ",
		('key', "F2"), " sort   ",
		('key', "F3"), " settings   ",
		]

	def __init__(self):
		"""
				Initializes the widget
		"""
		self.footer = Text(self.footer_text)
		super(Footer, self).__init__(self.footer, 'header')

# Testing
if __name__ == '__main__':
	listbox = ListBox(SimpleListWalker([]))
	view = Frame(listbox, header=None, footer=Footer())

	def exit(key):
		if key in ('q', 'Q'):
			raise ExitMainLoop()

	main_loop = MainLoop(view, palette, unhandled_input=exit)
	main_loop.run()
