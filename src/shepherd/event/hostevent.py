from . import Event

class HostEvent(Event):
    def __init__(self, **kwargs):
        super(HostEvent, self).__init__('host', **kwargs)
