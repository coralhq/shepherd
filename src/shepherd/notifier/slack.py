from shepherd.notifier import Notifier
from shepherd.event import Event
from slacker import Slacker

class Slack(Notifier):
    def __init__(self, *args, **kwargs):
        super(Slack, self).__init__(*args, **kwargs)
        self.token = self.config.SLACK_TOKEN
        self.channel = self.config.SLACK_CHANNEL
        self.slack = Slacker(self.token)

    def notify(self, event:Event):
        try:
            attachments = self._create_attachments(event)
            response = self.slack.chat.post_message(self.channel, '',
                  as_user=True, attachments=attachments)
            if response.body['ok']:
                self.log.debug("Notification sent to %s" % self.channel)
            else:
                self.log.error(response.body)
                raise Exception("Failed to send notification to %s" % self.channel)
        except Exception as e:
            import traceback
            self.log.error(traceback.format_exc())
            self.log.error(e)

    def _create_fields(self, event:Event):
        meta = event.meta()
        fields = []
        for key in meta.keys():
            val = meta[key]
            fields += [{
                "title": key.title(),
                "value": "`%s`" % val,
                "short": True
            }]

        return fields

    def _create_attachments(self, event:Event):
        return [{
                "fallback": event.description(),
                "color": event.severity(),
                "author_name": self.config.SLACK_AUTHOR_NAME,
                "author_icon": self.config.SLACK_AUTHOR_ICON,
                "text": event.summary(),
                "footer": self.config.SLACK_FOOTER,
                "footer_icon": self.config.SLACK_FOOTER_ICON,
                "mrkdwn_in": ["text", "fields"],
                "fields": self._create_fields(event)
            }]
