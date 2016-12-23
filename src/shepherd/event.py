SUPPORTED_TYPES = ['host', 'service']

def from_resource(res):
    event = {'type': res['type']}

    if res['type'] == 'host':
        event['name'] = res['hostname']
        event['state'] = res['agentState']
        cls = HostEvent
    elif res['type'] in ['service']:
        image = res.get('launchConfig',{}).get('imageUuid', '')
        event['name'] = res['name']
        event['state'] = res['state']
        event['image'] = image.replace('docker:', '', 1)
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

    def description(self):
        return "%s %s %s" % (self.type.title(), self.name, self.state)

    def summary(self):
        return self.description()

    def meta(self):
        return dict(self)

    def severity(self):
        return "default"

class ServiceEvent(Event):
    def __init__(self, image=None, **kwargs):
        super(ServiceEvent, self).__init__('service', **kwargs)
        self.image = image

    def __iter__(self):
        yield from super(ServiceEvent, self).__iter__()
        yield 'image', self.image

    def summary(self):
        return u"{} {}".format(self.type.title(), self.state)

    def meta(self):
        return {
            "name": self.name, "image": self.image
        }

    def severity(self):
        if self.state in ['upgraded', 'active']:
            return 'good'
        elif self.state in ['inactive']:
            return 'error'
        else:
            return 'default'

class HostEvent(Event):
    def __init__(self, **kwargs):
        super(HostEvent, self).__init__('host', **kwargs)
