from .event import Event
from .hostevent import HostEvent
from .serviceevent import ServiceEvent

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
