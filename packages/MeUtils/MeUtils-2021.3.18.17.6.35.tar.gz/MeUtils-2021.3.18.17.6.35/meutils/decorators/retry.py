#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : retry
# @Time         : 2021/3/18 2:57 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from tenacity import retry, wait_fixed


def wait_retry(n=3):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        @retry(wait=wait_fixed(n))
        def wait():
            logger.warning("retry")
            if wrapped(*args, **kwargs):
                return True

            raise Exception

        return wait()

    return wrapper


# from meutils.cmds import HDFS
# HDFS.check_path_isexist()

e = time.time() + 10
print(e)


@wait_retry(5)
def ff():
    return time.time() > e  # 变的


if __name__ == '__main__':
    print(ff())
