from . import helper as h

SUPPORTED_TYPES = ['host', 'service']

def from_resource(res):
    event = {'type': res['type']}

    if res['type'] == 'host':
        event['name'] = res['hostname']
        event['state'] = res['agentState']
        c = HostEvent
    elif res['type'] in ['service']:
        event['name'] = res['name']
        event['state'] = res['state']
        event['image'] = h.get(res, '.launchConfig.imageUuid').replace('docker:', '', 1)
        c = ServiceEvent

    return c(**event)

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


class ServiceEvent(Event):
    def __init__(self, image=None, **kwargs):
        super(ServiceEvent, self).__init__('service', **kwargs)
        self.image = image

    def __iter__(self):
        yield from super(ServiceEvent, self).__iter__()
        yield 'image', self.image

class HostEvent(Event):
    def __init__(self, **kwargs):
        super(HostEvent, self).__init__('host', **kwargs)
