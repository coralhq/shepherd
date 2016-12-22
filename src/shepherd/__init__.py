from . import helper as h
from .logging import log
from .event import from_resource, SUPPORTED_TYPES

def start(cfg):
    from websocket import WebSocketApp
    from simplejson import loads,dumps
    from rx import Observable
    from rx.subjects import Subject

    # create events stream
    # - p = payload
    # - r = resource
    stream = Subject()
    events = (stream
        .map(loads).filter(lambda p: p['name'] == 'resource.change')
        .map(lambda p: h.get(p, '.data.resource'))
            .filter(lambda r: isinstance(r,dict))
            .filter(lambda r: r['type'] in SUPPORTED_TYPES)
        .map(from_resource)
        .distinct_until_changed())

    # subscribe
    subs = []
    subs += [events.subscribe(log.debug)]
    subs += [events.subscribe()]

    # connect to websocket
    ws = WebSocketApp(cfg.RANCHER_WS_URL,
          on_message = lambda ws,msg: stream.on_next(msg),
          on_error = lambda ws,err: log.error(err),
          on_close = lambda ws: log.info('Websocket connection closed'),
          on_open = lambda ws: log.info('Websocket connection opened'),
          header = {"Authorization": cfg.RANCHER_WS_AUTH})
    ws.run_forever()

    # clean subscriptions
    for sub in subs:
        sub.dispose()
