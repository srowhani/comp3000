# Model/Process.py
# Generic model for a process
# http://www.tldp.org/LDP/tlk/kernel/processes.html
# Properties
#   cpu_perc -> Percentage of resources allocated in processer
#   state -> One of [Running]
#
class Process (object):
    RUNNING = 1
    WAITING = 2
    STOPPED = 3
    ZOMBIE  = 4
    def __init__(self, config = dict()):
        self.config = config

        self.cpu_perc = config.cpu_perc
        self.memory_alloc = config.memory_alloc
        self.current_state = config.cpu

        # Identifiers
        self.uid = config.uid
        self.gid = config.gid

        # Scheduling
        self.policy = config.policy

        # ... etc
    # Getters and Setters
    def get (attr):
        return self.config[attr]
    def set (attr, value):
        self.config[attr] = value
