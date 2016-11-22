import os
from ProcessList import ProcessList
from Palette import palette

from urwid import (
    Pile,
    Button,
    Columns,
    MainLoop,
    ListBox,
    SimpleListWalker,
    WidgetWrap,
    AttrMap,
    AttrWrap,
    BoxAdapter,
    ExitMainLoop
)

class ProcessTable(AttrMap):
    def __init__ (self, num_rows=20, w=(12, 8, 15, 10, 10, 10, 15)):
        """
            @method __init__
            Initializes the widget
        """
        self.m_process_list = ProcessList(w)

        self.w_status = Button('Status')
        self.w_pid = Button('PID')
        self.w_name = Button('Name')
        self.w_cpu = Button('CPU %')
        self.w_mem = Button('MEM %')
        self.w_up = Button('Uptime')
        self.w_pname = Button('Process')
        self.header_buttons = [
            self.w_status,
            self.w_pid,
            self.w_name,
            self.w_cpu,
            self.w_mem,
            self.w_up,
            self.w_pname
        ]
        for button in self.header_buttons:
            button._label.align = 'center'

        m_header = AttrMap(
            Columns([
                ('fixed', w[0], self.w_status),
                ('fixed', w[1], self.w_pid),
                ('fixed', w[2], self.w_name),
                ('fixed', w[3], self.w_cpu),
                ('fixed', w[4], self.w_mem),
                ('fixed', w[5], self.w_up),
                ('fixed', w[6], self.w_pname)
            ]), 'invert'
        )
        m_lb = ListBox(SimpleListWalker([
            m_header,
            BoxAdapter(self.m_process_list, num_rows)
        ]))
        super(ProcessTable, self).__init__(m_lb, None)
        self.update()

    def update (self):
        """
            @method update
            Handles updates and propogates
            update call to all child components
        """
        self.m_process_list.update()

"""
    Testing
"""
if __name__ == '__main__':
    pt = ProcessTable()

    def exit (p):
        if p is 'q':
            raise ExitMainLoop
    def refresh(loop, data):
        pt.update()
        loop.set_alarm_in(1, refresh)

    main_loop = MainLoop(pt, palette=palette, pop_ups=True, unhandled_input=exit)
    main_loop.set_alarm_in(1, refresh)

    main_loop.run()
