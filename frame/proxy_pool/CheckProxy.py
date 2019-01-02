# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     CheckProxy
   Description :   used for check getFreeProxy.py
   Author :        JHao
   date：          2018/7/10
-------------------------------------------------
   Change Activity:
                   2018/7/10: CheckProxy
-------------------------------------------------
"""

import sys
import logging
from getFreeProxy import GetFreeProxy
from utilFunction import verifyProxyFormat

sys.path.append('../')


class CheckProxy(object):

    @staticmethod
    def checkAllGetProxyFunc():
        """
        检查getFreeProxy所有代理获取函数运行情况
        Returns:
            None
        """
        import inspect
        member_list = inspect.getmembers(GetFreeProxy, predicate=inspect.isfunction)
        proxy_count_dict = dict()
        for func_name, func in member_list:
            logging.info(u"开始运行 {}".format(func_name))
            try:
                proxy_list = [_ for _ in func() if verifyProxyFormat(_)]
                proxy_count_dict[func_name] = len(proxy_list)
            except Exception as e:
                logging.info(u"代理获取函数 {} 运行出错!".format(func_name))
                logging.error(str(e))
        logging.info(u"所有函数运行完毕 " + "***" * 5)
        for func_name, func in member_list:
            logging.info(u"函数 {n}, 获取到代理数: {c}".format(n=func_name, c=proxy_count_dict.get(func_name, 0)))

    @staticmethod
    def checkGetProxyFunc(func):
        """
        检查指定的getFreeProxy某个function运行情况
        Args:
            func: getFreeProxy中某个可调用方法

        Returns:
            None
        """
        func_name = getattr(func, '__name__', "None")
        logging.info("start running func: {}".format(func_name))
        count = 0
        for proxy in func():
            if verifyProxyFormat(proxy):
                logging.info("{} fetch proxy: {}".format(func_name, proxy))
                count += 1
        logging.info("{n} completed, fetch proxy number: {c}".format(n=func_name, c=count))


if __name__ == '__main__':
    CheckProxy.checkAllGetProxyFunc()
    CheckProxy.checkGetProxyFunc(GetFreeProxy.freeProxyFirst)
