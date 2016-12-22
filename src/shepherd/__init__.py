from . import helper as h
from .logging import log
from .event import from_resource, SUPPORTED_TYPES
from .config import Config

def start(c:Config):
    from websocket import WebSocketApp
    from simplejson import loads,dumps
    from rx import Observable
    from rx.subjects import Subject
    from rx.concurrency import NewThreadScheduler

    from .notifier.slack import Slack
    slack = Slack(config=c, log=log)

    # create streams
    # - p = payload
    # - r = resource
    # - e = event
    stream = Subject()
    events = (stream
        .map(loads).filter(lambda p: p['name'] == 'resource.change')
        .map(lambda p: h.get(p, '.data.resource'))
            .filter(lambda r: isinstance(r,dict))
            .filter(lambda r: r['type'] in SUPPORTED_TYPES)
        .map(from_resource)
        .distinct_until_changed())
    slack_events = (events
        .filter(lambda e: e.type == 'service'))

    # subscribe
    async = NewThreadScheduler()
    subs = []
    subs += [events.subscribe(log.debug)]
    subs += [slack_events.observe_on(async).subscribe(slack.notify)]

    # connect to websocket
    ws = WebSocketApp(c.RANCHER_WS_URL,
          on_message = lambda ws,msg: stream.on_next(msg),
          on_error = lambda ws,err: log.error(err),
          on_close = lambda ws: log.info('Websocket connection closed'),
          on_open = lambda ws: log.info('Websocket connection opened'),
          header = {"Authorization": c.RANCHER_WS_AUTH})
    ws.run_forever()

    # clean subscriptions
    for sub in subs:
        sub.dispose()
