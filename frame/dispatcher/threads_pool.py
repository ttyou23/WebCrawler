# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 13:57
# @Author  : tianwei
# @Site    : 
# @File    : threads_pool.py
# @Software: PyCharm
import threading
from Queue import Queue

from frame.dispatcher import TPEnum


class ThreadPool(object):

    def __int__(self):

        self._number_dict = {
            TPEnum.TASKS_RUNNING: 0,                    # the count of tasks which are running

            TPEnum.URL_FETCH_NOT: 0,                    # the count of urls which haven't been fetched
            TPEnum.URL_FETCH_SUCC: 0,                   # the count of urls which have been fetched successfully
            TPEnum.URL_FETCH_FAIL: 0,                   # the count of urls which have been fetched failed
            TPEnum.URL_FETCH_COUNT: 0,                  # the count of urls which appeared in self._queue_fetch

            TPEnum.HTM_PARSE_NOT: 0,                    # the count of urls which haven't been parsed
            TPEnum.HTM_PARSE_SUCC: 0,                   # the count of urls which have been parsed successfully
            TPEnum.HTM_PARSE_FAIL: 0,                   # the count of urls which have been parsed failed

            TPEnum.ITEM_SAVE_NOT: 0,                    # the count of urls which haven't been saved
            TPEnum.ITEM_SAVE_SUCC: 0,                   # the count of urls which have been saved successfully
            TPEnum.ITEM_SAVE_FAIL: 0,                   # the count of urls which have been saved failed

            TPEnum.PROXIES_LEFT: 0,                     # the count of proxies which are avaliable
            TPEnum.PROXIES_FAIL: 0,                     # the count of proxies which banned by website
        }
        self._lock = threading.Lock()                   # the lock which self._number_dict needs

        self._fetch_queue = Queue()
        self._parse_queue = Queue()
        self._save_queue = Queue()

        self.__init_threading_pool(self.thread_num)

        return

    def add_fetch(self):
        return

    def add_parse(self):
        return

    def add_save(self):
        return