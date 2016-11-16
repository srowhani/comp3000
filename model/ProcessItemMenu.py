from urwid import (
    PopUpLauncher,
    WidgetWrap,
    Button,
    Pile,
    Text,
    AttrWrap,
    Filler,
    MainLoop,
    ListBox,
    SimpleListWalker,
    ExitMainLoop,
    connect_signal
)

class PopUpDialog(WidgetWrap):
    """A dialog that appears with nothing but a close button """
    signals = ['close']
    def __init__(self, item):
        close_button = Button("Dismiss")
        connect_signal(close_button, 'click',
            lambda button:self._emit("close"))
        pile = Pile([Text(str(item)), close_button])
        self.__super.__init__(AttrWrap(Filler(pile), 'popbg'))

class ProcessPopUp (PopUpLauncher):
    def __init__(self, button, item):
        self.__super.__init__(button)
        self.item = item
    def open (self, item=None):
        self.open_pop_up()
    def create_pop_up (self):
        p = PopUpDialog(self.item)
        connect_signal(p, 'close',
            lambda button: self.close_pop_up())
        return p
    def get_pop_up_parameters(self):
        return {'left':0, 'top':1, 'overlay_width':80, 'overlay_height':20}
"""
    Testing
"""
if __name__ == '__main__':
    b = Button('click me')

    popup = ProcessPopUp(b, Text('test content'))
    connect_signal(b, 'click', lambda x: popup.open())
    proc = AttrWrap(popup, None)
    lb = ListBox(SimpleListWalker([proc]))

    def exit (p):
        if p is 'q':
            raise ExitMainLoop

    m = MainLoop(
        lb,
        palette=[('reversed', 'standout', ''), ('popbg', 'white', 'dark blue')],
        pop_ups=True,
        unhandled_input=exit
    )
    m.run()
