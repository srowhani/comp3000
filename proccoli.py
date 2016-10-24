#!/usr/bin/python
#
# Contributors
#   Seena Rowhani 100945353
#   Shane Slatter 100946497
#
# Description
#   A process manager written in python

# System Tools
import os
import sys

# Utilities
from operator import isNumberType
from getopt import getopt, error as OptionsError

# Getting Started
#  https://github.com/seb-m/pyinotify/wiki/Handling-Events
# Event Types
#  https://github.com/seb-m/pyinotify/wiki/Events-types
from pyinotify import WatchManager, ProcessEvent, AsyncNotifier

# Async Library
import asyncore

class Proccoli (ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname
    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname
    def process_IN_MODIFY(self, event):
        print "Modifying:", event

def main():
    try:
        opts, args = getopt(sys.argv[1:], 'h', ['help'])
    except OptionsError, error_msg:
        print error_msg
        print 'For more information try --help'
        return 2

    # Initialization
    proc_directory = os.list('/proc')

    # TODO: dict() could be better for modifications
    processes = [int(i) for i in proc_directory if i.isdigit()]

    wm = WatchManager()
    notif = AsyncNotifier(wm, Proccoli)
    # Be able to differentiate different events coherently
    watch_dog = wm.add_watch('/proc', mask, rec=True)

    asyncore.loop()
    return 0

if __name__ == '__main__':
    sys.exit(main())
