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
