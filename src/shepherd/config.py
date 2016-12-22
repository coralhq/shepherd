from base64 import b64encode
from os import environ as env
from dotenv import load_dotenv

class Config(object):
    def __init__(self, dotenv='.env'):
        super(Config, self).__init__()
        load_dotenv('.env')

        self.RANCHER_SSL = env.get('RANCHER_SSL','').lower() == 'true'
        self.RANCHER_ACCESS_KEY = env.get('RANCHER_ACCESS_KEY', None)
        self.RANCHER_SECRET_KEY = env.get('RANCHER_SECRET_KEY', None)
        self.RANCHER_HOST = env.get('RANCHER_HOST', None)
        self.RANCHER_PROJECT_ID = env.get('RANCHER_PROJECT_ID', None)
        self.RANCHER_PROJECT_NAME = env.get('RANCHER_PROJECT_NAME', self.RANCHER_PROJECT_ID)
        self.SLACK_TOKEN = env.get('SLACK_TOKEN', None)
        self.SLACK_CHANNEL = env.get('SLACK_CHANNEL', None)

        self.RANCHER_PROTOCOL = 'wss' if self.RANCHER_SSL else 'ws'
        self.RANCHER_WS_URL = "{}://{}/v1/projects/{}/subscribe?eventNames=resource.change".format(
                         self.RANCHER_PROTOCOL,
                         self.RANCHER_HOST,
                         self.RANCHER_PROJECT_ID
                         )
        self.RANCHER_WS_AUTH = "{}:{}".format(self.RANCHER_ACCESS_KEY, self.RANCHER_SECRET_KEY)
        self.RANCHER_WS_AUTH = b64encode(self.RANCHER_WS_AUTH.encode('utf-8')).decode('utf-8')
        self.RANCHER_WS_AUTH = "Basic {}".format(self.RANCHER_WS_AUTH)

        self.required = {
            'RANCHER_ACCESS_KEY': self.RANCHER_ACCESS_KEY,
            'RANCHER_SECRET_KEY': self.RANCHER_SECRET_KEY,
            'RANCHER_HOST': self.RANCHER_HOST,
            'RANCHER_PROJECT_ID': self.RANCHER_PROJECT_ID,
            'SLACK_TOKEN': self.SLACK_TOKEN,
            'SLACK_CHANNEL': self.SLACK_CHANNEL,
        }

    def check(self, log):
        errors = []
        for key in self.required.keys():
            val = self.required[key]
            if not val:
                log.error("%s is required" % key)
        if errors:
            raise Exception("Configuration error")

    def info(self, log):
        log.info("---")
        log.info("HOST: %s", self.RANCHER_HOST)
        log.info("ENVIRONMENT: %s (%s)", self.RANCHER_PROJECT_NAME, self.RANCHER_PROJECT_ID)
        log.info("SSL: %s", self.RANCHER_SSL)
        log.info("---")
