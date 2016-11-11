# Model/Process.py
# Generic model for a process
# http://www.tldp.org/LDP/tlk/kernel/processes.html
# Properties
#   cpu_perc -> Percentage of resources allocated in processer
#   state -> One of [Running]
#
from Component import GenericComponent
class Process (GenericComponent):

    def __init__(self):
        super(GenericComponent, self)
        print(self.toString())

a = Process()
