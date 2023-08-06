# coding: utf-8

import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_dingding
from .forms import DingDingOptionsForm

DingTalk_API = "https://oapi.dingtalk.com/robot/send?access_token={token}"


class DingDingPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to DingDing.
    """
    author = 'dreamerldq'
    author_url = 'https://github.com/dreamerldq/sentry-dingding-format'
    version = '1.0.24'
    description = 'Send project error counts to DingDing .'
    resource_links = [
        ('Source', 'https://github.com/dreamerldq/sentry-dingding-format'),
        ('Bug Tracker', 'https://github.com/dreamerldq/sentry-dingding-format/issues'),
        ('README', 'https://github.com/dreamerldq/sentry-dingding-format/blob/master/README.md'),
    ]

    slug = 'WbDingDing'
    title = 'WbDingDing'
    conf_key = slug
    conf_title = title
    project_conf_form = DingDingOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def getGroupCount(self, groupId):
        headers={
            "Authorization": 'Bearer {token}'.format(token='4723370af03c4c95bc3bb0570fef1da3c5a2277477544571b827daceccbc3276')    
        }
        url = 'http://localhost:9000/api/0/issues/{groupId}/'.format(groupId=groupId )
        r = requests.get(url,headers=headers).json()
        return r["count"]

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """

        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        count = self.getGroupCount(group.id)

        access_token = self.get_option('access_token', group.project)
        send_url = DingTalk_API.format(token=access_token)
        title = u'【%s】的项目异常' % event.project.slug

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": u"#### {title} \n\n > {message} \n\n > 设备:{device} \n\n > 数量:{count} \n\n > UID:{uid} \n\n > {path} \n\n [详细信息]({url})".format(
                    title=title,
                    device=event.get_tag('device'),
                    uid=event.get_tag('uid'),
                    path=event.get_tag('url'),
                    count=count,
                    message=event.title or event.message,
                    url=u"{}events/{}/".format(group.get_absolute_url(), event.event_id),
                )
            }
        }
        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )
