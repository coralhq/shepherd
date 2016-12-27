from .logging import log
from .event import from_resource, SUPPORTED_TYPES
from .config import Config

def start(c:Config):
    from websocket import WebSocketApp
    from simplejson import loads,dumps
    from rx import Observable
    from rx.subjects import Subject
    from rx.concurrency import NewThreadScheduler

    from .notifier import Slack, Jenkins
    slack = Slack(config=c, log=log)
    jenkins = Jenkins(config=c, log=log)

    # create streams
    stream = Subject()
    events = (stream
        .map(loads).filter(lambda p: p.get('name') == 'resource.change')
        .map(lambda payload: payload.get('data',{}))
            .filter(lambda data: isinstance(data, dict))
        .map(lambda data: data.get('resource',{}))
            .filter(lambda res: isinstance(res,dict))
            .filter(lambda res: res.get('type') in SUPPORTED_TYPES)
        .map(from_resource)
        .distinct_until_changed())
    slack_events = (events
        .filter(lambda event: event.type == 'service' and event.state == 'upgraded'))
    jenkins_events = (events
        .filter(lambda event: event.type == 'host' and event.state == 'reconnecting'))

    # subscribe
    async = NewThreadScheduler()
    subs = []
    subs += [events.subscribe(log.debug)]
    subs += [slack_events.observe_on(async).subscribe(slack.notify)]
    subs += [jenkins_events.observe_on(async).subscribe(jenkins.notify)]

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
