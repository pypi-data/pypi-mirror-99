#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : pipe_utils
# @Time         : 2020/11/12 11:35 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import functools
from meutils.common import *


class Pipe(object):
    """I am very like a linux pipe"""

    def __init__(self, function):
        self.function = function
        functools.update_wrapper(self, function)

    def __ror__(self, other):
        return self.function(other)

    def __call__(self, *args, **kwargs):
        return Pipe(lambda x: self.function(x, *args, **kwargs))


########### 常用管道函数
# 进度条
xtqdm = Pipe(lambda iterable, desc=None: tqdm(iterable, desc))

# base types
xtuple, xlist, xset = Pipe(tuple), Pipe(list), Pipe(set)

# 高阶函数
xmap = Pipe(lambda iterable, func: map(func, iterable))
xreduce = Pipe(lambda iterable, func: reduce(func, iterable))
xfilter = Pipe(lambda iterable, func: filter(func, iterable))

# itertools: https://blog.csdn.net/weixin_43193719/article/details/87536371
xchain = Pipe(lambda iterable: itertools.chain(*iterable))
xbatch = Pipe(lambda iterable, i=0, batch_size=1: itertools.islice(iterable, i * batch_size, (i + 1) * batch_size))

"""多个df: 
dfs = (
    Path('.').glob('demo*.txt') | xmap(lambda p: pd.read_csv(p, chunksize=2, names=['id'])) | xchain
)
"""
# str
xjoin = Pipe(lambda chars, sep=' ': sep.join(chars))
xsort = Pipe(lambda iterable, reverse=False: sorted(iterable, reverse=False))
xgetitem = Pipe(lambda iterable, index=0: operator.getitem(iterable, index))

xprint = Pipe(lambda s, sep='\n': print(s, sep=sep))


# np


# multiple
@Pipe
def xThreadPoolExecutor(iterable, func, max_workers=5):
    """
    with ThreadPoolExecutor(max_workers) as pool:
        pool.map(func, iterable)
    """
    with ThreadPoolExecutor(max_workers) as pool:
        return pool.map(func, iterable)


@Pipe
def xProcessPoolExecutor(iterable, func, max_workers=5):
    """
    with ProcessPoolExecutor(max_workers) as pool:
        pool.map(func, iterable)
    """
    with ProcessPoolExecutor(max_workers) as pool:
        return pool.map(func, iterable)


# operator: 排序、取多个值     https://blog.csdn.net/u010339879/article/details/98304292
# operator.itemgetter(*keys)(dic)
@Pipe
def xDictValues(keys, dic: dict, default=None):
    return tuple(dic.get(k, default) for k in keys)


@Pipe
def xDictRemove(keys, dic: dict):
    for k in keys:
        if k in dic:
            del dic[k]


if __name__ == '__main__':
    @Pipe
    def xfunc1(x):
        _ = x.split()
        print(_)
        return _


    @Pipe
    def xfunc2(x):
        _ = '>>'.join(x)
        print(_)
        return _


    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger.patch(lambda r: r.update(name='__file__', function=func.__name__)).info("Wrapped!")
            return func(*args, **kwargs)

        return wrapped


    # log = 'I am very like a linux pipe' | xfunc1 | xfunc2
    # logger.info(log)
    #
    # logger = logger.patch(lambda r: r.update(name=__file__, function=''))  # main:module
    # logger.info(log)
    #
    # # logger = logger.patch(wrapper(lambda x: ''))
    # # logger.info(log)

    ['aaaa', 'vvvvv'] | xprint
