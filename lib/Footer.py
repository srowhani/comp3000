from Palette import *
from urwid import (
    AttrMap, 
    AttrWrap, 
    Button, 
    Columns, 
    connect_signal, 
    ExitMainLoop, 
    Filler, 
    Frame, 
    ListBox, 
    MainLoop, 
    Padding, 
    Pile, 
    PopUpLauncher, 
    Text, 
    WidgetWrap
)
# reference https://github.com/urwid/urwid/blob/master/examples/pop_up.py
class HelpButton(PopUpLauncher):

  def __init__(self):
    """
      Initializes the widget
    """
    btn = Button('help')
    connect_signal(btn, 'click',
      lambda button: self.open_pop_up())
    super(HelpButton, self).__init__(btn)

  def create_pop_up(self):
    """
      Called each time the pop-up is opened
    """
    pop_up = HelpWindow()
    connect_signal(pop_up, 'close',
      lambda button: self.close_pop_up())
    return pop_up

  def get_pop_up_parameters(self):
    """
      Called each time the widget is rendered
    """
    return {'left':0, 'top':-15, 'overlay_width':50, 'overlay_height':20}

class HelpWindow(WidgetWrap):
  # Constants
  signals = ['close']
  help_text = [
    "Help Window\n\n",
    "Press 'q' or 'Q' to quit.\n",
    "Click on a process for options.\n\n",
    "%cpu(s)  a / b [ c ].\n",
    " a: combined un-niced and niced percentage.\n",
    " b: system percentage.\n",
    " c: visual graph of total percentage.\n\n",
    "Mem/Swap:  a / b [ c ].\n",
    " a: total used in gigabytes.\n",
    " b: total available in gigabytes.\n",
    " c: visual graph of total used.\n",
    ]

  def __init__(self):
    """
      Initializes the widget
    """
    close_button = Button("close")
    connect_signal(close_button, 'click',
      lambda button: self._emit('close'))
    help_window = Pile([
      Padding(Text(self.help_text), 'center', width=('relative', 90)), 
      Padding(AttrMap(close_button, 'popbg'), 'center', 9)
      ])
    super(HelpWindow, self).__init__(AttrWrap(Filler(help_window), 'progress'))

class Footer(AttrMap):
  # Constants
  footer_text = [
    " ",
    ("key", "q"), " quit ",
    ]

  def __init__(self):
    """
        Initializes the widget
    """
    self.footer_btn = HelpButton()
    self.footer = Columns([
      ('fixed', 10, Text(self.footer_text, align='left')), 
      ('fixed', 10, Padding(AttrMap(self.footer_btn, 'popbg'),'center', 8)),
      ])
    super(Footer, self).__init__(self.footer, 'header')

# Testing
if __name__ == '__main__':
  lb = ListBox([Text("Test")])
  view = Frame(lb, header=None, footer=Footer())

  def exit(key):
    if key in ('q', 'Q'):
      raise ExitMainLoop

  main_loop = MainLoop(view, palette, unhandled_input=exit, pop_ups=True)
  main_loop.run()
