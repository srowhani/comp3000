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
    connect_signal,
    ExitMainLoop
)
class HeaderButton(Button):
    def __init__ (self, label, key, handle_click):
        self.key = key
        self.original_label = label
        self.desc = False
        self.cb = handle_click
        connect_signal(self, 'click', handle_click)
        super(HeaderButton, self).__init__(label)

        self._label.align = 'center'

    def activate (self):
        return (self.key, self.set_order(not self.desc))
    def set_order (self, s):
        self.desc = s
        if self.desc:
            self.set_label(self.original_label + " [v]")
        else:
            self.set_label(self.original_label + " [^]")
        return self.desc
    def revert (self):
        self.set_label(self.original_label)

class ProcessTable(AttrMap):
    def __init__ (self, num_rows=20, w=(14, 14, 18, 16, 16, 16, 20)):
        """
            @method __init__
            Initializes the widget
        """
        self.m_process_list = ProcessList(w)
        self.prev_sort_item = None

        self.w_status = HeaderButton('Status', 'status', self.handle_click)
        self.w_pid = HeaderButton('PID', 'pid', self.handle_click)
        self.w_name = HeaderButton('Name', 'name', self.handle_click)
        self.w_cpu = HeaderButton('CPU %', 'cpu_perc', self.handle_click)
        self.w_mem = HeaderButton('MEM %', 'mem_perc', self.handle_click)
        self.w_up = HeaderButton('Uptime', 'uptime', self.handle_click)
        self.w_pname = HeaderButton('Process', 'pname', self.handle_click)

        self.w_cpu.activate()
        self.prev_sort_item = self.w_cpu
        
        self.header_buttons = h = [
            self.w_status,
            self.w_pid,
            self.w_name,
            self.w_cpu,
            self.w_mem,
            self.w_up,
            self.w_pname
        ]

        m_header = AttrMap(
            Columns(
                [('fixed', w[i], h[i]) for i in range(0, len(h))]
            ),
            'invert'
        )
        m_lb = ListBox(SimpleListWalker([
            m_header,
            BoxAdapter(self.m_process_list, num_rows)
        ]))
        super(ProcessTable, self).__init__(m_lb, None)
        self.update()
    def handle_click (self, item):
        if self.prev_sort_item:
            self.prev_sort_item.revert()
        key, order = item.activate()
        self.m_process_list.set_sort(key, order)
        self.prev_sort_item = item
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
