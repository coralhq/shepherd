from . import Event

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
