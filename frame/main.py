# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 15:59
# @Author  : tianwei
# @Site    : 
# @File    : main.py
# @Software: PyCharm

from dispatcher import *
from instances import *
from tools import  *


def test_heard(a):
    print "heard=======%s"%a
    return


def test_end(b):
    print "end======%s"%b
    return


if __name__ == '__main__':
    print "====================================开始=========================================="
    # spider = WebSpider()
    data = []
    data.append((test_heard, ["index %d"%i for i in range(10)]))
    data.append((test_end, ["flag %d" % i for i in range(10)]))
    print data
    for func_callback, listdata in data:
        if func_callback and listdata:
            for str in listdata:
                func_callback(str)
    print "====================================结束=========================================="
    pass
