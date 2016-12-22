from shepherd.notifier import Notifier
from shepherd.event import Event
from shepherd.event import LEVEL_INFO, LEVEL_SUCCESS, LEVEL_ERROR, LEVEL_WARNING
from slacker import Slacker

_colors = {
    LEVEL_INFO: 'default',
    LEVEL_SUCCESS: 'good',
    LEVEL_ERROR: 'danger',
    LEVEL_WARNING: 'warning',
}

class Slack(Notifier):
    def __init__(self, *args, **kwargs):
        super(Slack, self).__init__(*args, **kwargs)
        self.token = self.config.SLACK_TOKEN
        self.channel = self.config.SLACK_CHANNEL
        self.slack = Slacker(self.token)

    def notify(self, event:Event):
        try:
            attachments = self._attachments_from_event(event)
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

    def _attachments_from_event(self, event:Event):
        return [{
                "fallback": event.plain(),
                "color": _colors.get(event.severity(), LEVEL_INFO),
                "author_name": self.config.SLACK_AUTHOR_NAME,
                "author_icon": self.config.SLACK_AUTHOR_ICON,
                "title": event.title().upper(),
                "text": event.description(),
                "footer": self.config.SLACK_FOOTER,
                "footer_icon": self.config.SLACK_FOOTER_ICON
            }]
