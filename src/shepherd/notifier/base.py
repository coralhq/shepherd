from shepherd.event import Event
from shepherd.config import Config
from logging import Logger

class Notifier(object):
    def __init__(self, config:Config, log:Logger, *args, **kwargs):
        super(Notifier, self).__init__()
        self.config = config
        self.log = log

    def notify(self, event:Event):
        pass
