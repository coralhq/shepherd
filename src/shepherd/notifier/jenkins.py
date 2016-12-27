from shepherd.notifier import Notifier
from shepherd.event import Event
from jenkins import Jenkins as JenkinsServer

class Jenkins(Notifier):
    def __init__(self, *args, **kwargs):
        super(Jenkins, self).__init__(*args, **kwargs)
        self.url = self.config.JENKINS_URL
        self.username = self.config.JENKINS_USERNAME
        self.password = self.config.JENKINS_PASSWORD
        self.job_name = self.config.JENKINS_JOB_NAME
        self.job_token = self.config.JENKINS_JOB_TOKEN
        self.jenkins = JenkinsServer(self.url,
                                     username=self.username,
                                     password=self.password)

    def notify(self, event:Event):
        try:
            self.jenkins.build_job(self.job_name, dict(event), token=self.job_token)
            self.log.debug("Notification sent to %s/job/%s" % (self.url, self.job_name))
        except Exception as e:
            import traceback
            self.log.error(traceback.format_exc())
            self.log.error(e)
