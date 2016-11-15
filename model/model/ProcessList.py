import os
from ProcessListWalker import ProcessListWalker as pl
from urwid import ListBox, MainLoop, ExitMainLoop


class ProcessList(ListBox):
    m_walker = None
    def __init__ (self):
        """
            @method __init__
            Initializes the widget
        """
        self.m_walker = pl()
        super(ProcessList, self).__init__(self.m_walker)
        self.update()

    def update (self):
        """
            @method update
            Handles updates and propogates
            update call to all child components
        """
        self.m_walker.update()

"""
    Testing
"""
if __name__ == '__main__':
    pl = ProcessList()

    def exit (p):
        if p is 'q':
            raise ExitMainLoop
    def refresh(loop, data):
        pl.update()
        loop.set_alarm_in(1, refresh)

    main_loop = MainLoop(pl, palette=[('reversed', 'standout', '')], unhandled_input=exit)
    main_loop.set_alarm_in(1, refresh)

    main_loop.run()
