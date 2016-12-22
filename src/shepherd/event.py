from . import helper as h

SUPPORTED_TYPES = ['host', 'service']

LEVEL_SUCCESS = 'success'
LEVEL_INFO = 'info'
LEVEL_WARNING = 'warning'
LEVEL_ERROR = 'error'

def from_resource(res):
    event = {'type': res['type']}

    if res['type'] == 'host':
        event['name'] = res['hostname']
        event['state'] = res['agentState']
        cls = HostEvent
    elif res['type'] in ['service']:
        event['name'] = res['name']
        event['state'] = res['state']
        event['image'] = h.get(res, '.launchConfig.imageUuid').replace('docker:', '', 1)
        cls = ServiceEvent

    return cls(**event)

class Event(object):
    def __init__(self, event_type, name=None, state=None, **kwargs):
        self.type = event_type
        self.name = name
        self.state = state

    def __iter__(self):
        yield 'type', self.type
        yield 'name', self.name
        yield 'state', self.state

    def __str__(self):
        return str(dict(self))

    def __eq__(self, other):
        return self.__dict__ == other

    def plain(self):
        return "%s: %s %s" % (self.type, self.name, self.state)

    def title(self):
        return self.name

    def description(self):
        return self.state

    def severity(self):
        return LEVEL_INFO

class ServiceEvent(Event):
    def __init__(self, image=None, **kwargs):
        super(ServiceEvent, self).__init__('service', **kwargs)
        self.image = image

    def __iter__(self):
        yield from super(ServiceEvent, self).__iter__()
        yield 'image', self.image

    def description(self):
        return u"{} - {}".format(self.state, self.image)

    def severity(self):
        if self.state == 'upgraded':
            return LEVEL_SUCCESS
        elif self.state == 'inactive':
            return LEVEL_ERROR
        else:
            return LEVEL_INFO

class HostEvent(Event):
    def __init__(self, **kwargs):
        super(HostEvent, self).__init__('host', **kwargs)
