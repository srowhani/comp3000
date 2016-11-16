import os, signal
from Palette import palette
import Process
from urwid import (
    PopUpLauncher,
    WidgetWrap,
    Button,
    Pile,
    Text,
    AttrMap,
    Filler,
    MainLoop,
    ListBox,
    SimpleFocusListWalker,
    ExitMainLoop,
    connect_signal,
    Columns
)


class MenuOption(Button):
    def __init__ (self, signal, on_select):
        self.on_select = on_select
        self.signal = signal
        connect_signal(self, 'click', on_select)
        super(MenuOption, self).__init__("%d - %s" % (signal[1], signal[0]))

    def get_text (self):
        return self.signal[0]
    def keypress (self, size, key):
        """
            @Override urwid.Widget
            @method keypress
            @param size - size of the widget taking in the keypress
            @param key  - char repr the key which was pressed
            Propogate navigation to PopupDialog
        """
        if key is 'enter':
            self.on_select(self)
        return key
    def selectable (self):
        return True


class PopUpDialog(WidgetWrap):
    """A dialog that appears with nothing but a close button """
    signals = ['close']
    def __init__ (self, proc):
        self.proc = proc
        dismiss = Button("Dismiss")
        connect_signal(dismiss, 'click',
            lambda button: self._emit("close"))
        signal_list = [i for i in signal.__dict__.items() if 'SIG' in i[0]]
        signal_list.sort(key = lambda x: x[1])
        items = [MenuOption(t, self.on_item_select) for t in signal_list]
        items = Pile(items)
        pile = Pile([
            dismiss,
            items
        ])

        self.c = AttrMap(Filler(pile), 'popbg')

        self.__super.__init__(self.c)

    def on_item_select(self, item):
        """
            Handle on option click
        """
        try:
            os.kill(self.proc.get_pid(), int(signal.__dict__[item.get_text()]))
            self._emit('close')
        except:
            """ Show Error Dialog """

class ProcessItemDialog (PopUpLauncher):
    """ Item menu for a given process """

    def __init__ (self, button, item):
        """
            @method __init__
            @param button: Button passed in to handle click to launch
            @param item: Process instance the popup corresponds to.
        """
        self.__super.__init__(button)
        self.item = item
    def open (self, item=None):
        """
            @method open
            Alias to PopUpLauncher.open_pop_up
        """
        self.open_pop_up()
    def create_pop_up (self):
        p = PopUpDialog(self.item)
        connect_signal(p, 'close',
            lambda button: self.close_pop_up())
        return p
    def get_pop_up_parameters (self):
        return {'left':0, 'top':1, 'overlay_width':30, 'overlay_height':20}
"""
    Testing
"""
if __name__ == '__main__':
    b = Button('click me')
    p1 = Process.Process(1, lambda x: x, lambda: x)
    popup = ProcessItemDialog(b, p1)
    connect_signal(b, 'click', lambda x: popup.open())
    proc = AttrMap(popup, None)
    lb = ListBox(SimpleFocusListWalker([proc]))

    def exit (p):
        if p is 'q':
            raise ExitMainLoop

    m = MainLoop(
        lb,
        palette=palette,
        pop_ups=True,
        unhandled_input=exit
    )
    m.run()
