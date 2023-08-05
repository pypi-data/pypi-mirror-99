#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : crontab
# @Time         : 2021/2/7 5:33 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
# @Warning      : job.slices = ''  # 不再重复添加时间 * * * * *

from meutils.pipe import *
from meutils.zk_utils import get_zk_config


class Cron(object):
    """
    Crontab 增删改查
    """

    def __init__(self, **kwargs):
        pass

    def add(self, command, comment):
        with CronTab(True) as cron:
            logger.warning(f"ADD cron: {command}")
            job = cron.new(command, comment, pre_comment=True)
            job.slices = ''  # 不再重复添加时间 * * * * *

    def remove(self, comment):
        """

        :param comment: 仅支持comment剔除
        :return:
        """
        with CronTab(True) as cron:
            jobs = cron.find_comment(comment)
            for job in jobs:
                cron.remove(job)

    def update_from_file(self, path):
        """从zk同步cron: 可配置每天最后一分钟同步crontab配置信息（zk/yaml） 59 23 * * *


        :param path: zk/yaml /mipush/crontab/mitv
            comment1:
              - cmd1
              - cmd2
        :return:
        """
        crontabs = yaml_load(path) if Path('path').is_file() else get_zk_config(path)
        logger.info(f"Crontab update to: {bjson(crontabs)}")

        # todo: 统一管理统一前缀的， filter(lambda prefix: str.startswith(prefix), _comments)
        with CronTab(True) as cron:
            for comment, cmds in crontabs.items():
                # 删除
                jobs = cron.find_comment(comment)
                for job in jobs:
                    cron.remove(job)

                # 新增
                for cmd in cmds:
                    cmd = cmd.strip().split() | xjoin
                    job = cron.new(cmd, comment, pre_comment=True)  # cmd里特殊字符处理
                    job.slices = ''  # 不再重复添加时间 * * * * *


def main():
    fire.Fire(Cron)
