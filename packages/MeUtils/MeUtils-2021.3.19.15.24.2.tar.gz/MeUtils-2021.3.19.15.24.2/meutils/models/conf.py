#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : confs
# @Time         : 2021/2/7 8:19 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


from meutils.models import BaseConfig


class WebhooksConf(BaseConfig):
    _path = '/mipush/bot/webhooks'

    logger = ''
    PUSH平台报警机器人 = ''
    小米视频与多看PUSH监控 = ''


if __name__ == '__main__':
    WebhooksConf.init()
