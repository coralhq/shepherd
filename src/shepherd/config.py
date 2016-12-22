from base64 import b64encode
from os import environ as env
from dotenv import load_dotenv
from os.path import isfile

class Config(object):
    def __init__(self, log, dotenv='.env'):
        super(Config, self).__init__()

        self.log = log

        if dotenv and isfile(dotenv):
            log.info('Loading config from %s', dotenv)
            load_dotenv(dotenv)

        # required configs
        self.RANCHER_SSL = env.get('RANCHER_SSL','').lower() == 'true'
        self.RANCHER_ACCESS_KEY = env.get('RANCHER_ACCESS_KEY', None)
        self.RANCHER_SECRET_KEY = env.get('RANCHER_SECRET_KEY', None)
        self.RANCHER_HOST = env.get('RANCHER_HOST', None)
        self.RANCHER_PROJECT_ID = env.get('RANCHER_PROJECT_ID', None)
        self.RANCHER_PROJECT_NAME = env.get('RANCHER_PROJECT_NAME', self.RANCHER_PROJECT_ID)
        self.SLACK_TOKEN = env.get('SLACK_TOKEN', None)
        self.SLACK_CHANNEL = env.get('SLACK_CHANNEL', None)

        # optional configs
        self.SLACK_FOOTER = env.get('SLACK_FOOTER', None)
        self.SLACK_FOOTER_ICON = env.get('SLACK_FOOTER_ICON', None)
        self.SLACK_AUTHOR_NAME = env.get('SLACK_AUTHOR_NAME', None)
        self.SLACK_AUTHOR_ICON = env.get('SLACK_AUTHOR_ICON', None)

        # derived configs
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

    def check(self):
        errors = []
        for key in self.required.keys():
            val = self.required[key]
            if not val:
                self.log.error("%s is required" % key)
        if errors:
            raise Exception("Configuration error")

    def info(self):
        self.log.info("---")
        self.log.info("HOST: %s", self.RANCHER_HOST)
        self.log.info("ENVIRONMENT: %s (%s)", self.RANCHER_PROJECT_NAME, self.RANCHER_PROJECT_ID)
        self.log.info("SSL: %s", self.RANCHER_SSL)
        self.log.info("---")
