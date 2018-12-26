# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 13:57
# @Author  : tianwei
# @Site    : 
# @File    : threads_pool.py
# @Software: PyCharm
import logging
import threading
from Queue import Queue

from .thread_inst import *
from instances import *
from tools import *


class ThreadPool(object):

    def __init__(self, parse_inst, save_inst=None, proxieser=None, fetch_inst=None, max_count_parsave=100, max_count_proxies=100):

        self._number_dict = {
            TPEnum.TASKS_RUNNING: 0,  # the count of tasks which are running

            TPEnum.URL_FETCH_NOT: 0,  # the count of urls which haven't been fetched
            TPEnum.URL_FETCH_SUCC: 0,  # the count of urls which have been fetched successfully
            TPEnum.URL_FETCH_FAIL: 0,  # the count of urls which have been fetched failed
            TPEnum.URL_FETCH_COUNT: 0,  # the count of urls which appeared in self._queue_fetch

            TPEnum.HTM_PARSE_NOT: 0,  # the count of urls which haven't been parsed
            TPEnum.HTM_PARSE_SUCC: 0,  # the count of urls which have been parsed successfully
            TPEnum.HTM_PARSE_FAIL: 0,  # the count of urls which have been parsed failed

            TPEnum.ITEM_SAVE_NOT: 0,  # the count of urls which haven't been saved
            TPEnum.ITEM_SAVE_SUCC: 0,  # the count of urls which have been saved successfully
            TPEnum.ITEM_SAVE_FAIL: 0,  # the count of urls which have been saved failed

            TPEnum.PROXIES_LEFT: 0,  # the count of proxies which are avaliable
            TPEnum.PROXIES_FAIL: 0,  # the count of proxies which banned by website
        }

        self._lock = threading.Lock()  # the lock which self._number_dict needs
        self._url_filter = UrlFilter() #URL

        self._thread_stop_flag = False  # default: False, stop flag of threads
        self._fetcher_number = 0  # default: 0, fetcher number in thread pool
        self._max_count_parsave = max_count_parsave         # maximum count of items which in parse queue or save queue
        self._max_count_proxies = max_count_proxies         # maximum count of items which in proxies queue

        self._queue_fetch = Queue()
        self._queue_parse = Queue()
        self._queue_saver = Queue()
        self._queue_proxies = Queue()  # {"http": "http://auth@ip:port", "https": "https://auth@ip:port"}

        self._inst_fetcher = fetch_inst if fetch_inst else Fetcher()
        self._inst_parse = parse_inst
        self._inst_saver = save_inst if save_inst else Saver()
        self._inst_proxieser = proxieser if proxieser else Proxieser()

        self._thread_fetch_list = []
        self._thread_parse = None
        self._thread_save = None
        self._thread_proxieser = None

        self._thread_moniter = MoniterThread("MoniterThread", self)

        return

    ## ===================================================================================================================

    def start_working(self, root_url, fetcher_num):

        self._fetcher_number = fetcher_num
        self._thread_stop_flag = False

        self.add_a_task(TPEnum.URL_FETCH, (root_url, None, 0))
        logging.info("ThreadPool starts working: urls_count=%s, fetcher_num=%s",
                     self.get_number_dict(TPEnum.URL_FETCH_NOT), fetcher_num)
        self._thread_fetch_list = [FetchThread("FetchThread %d"%i, self._inst_fetcher, self) for i in
                                   xrange(fetcher_num)]
        self._thread_parse = ParseThread("ParseThread", self._inst_parse, self)
        self._thread_save = SaveThread("SaveThread", self._inst_saver, self)
        self._thread_proxieser = ProxiesThread("ProxiesThread", self._inst_proxieser, self)

        if self._thread_moniter:
            self._thread_moniter.setDaemon(True)
            self._thread_moniter.start()

        for thread in self._thread_fetch_list:
            thread.setDaemon(True)
            thread.start()

        if self._thread_parse:
            self._thread_parse.setDaemon(True)
            self._thread_parse.start()

        if self._thread_save:
            self._thread_save.setDaemon(True)
            self._thread_save.start()
        logging.info("ThreadPool starts working: success")
        return

    def wait_for_finish(self):

        self._thread_stop_flag = True

        for thread in filter(lambda x: x.is_alive(), self._thread_fetch_list):
            thread.join()

        if self._thread_parse and self._thread_parse.is_alive():
            self._thread_parse.join()

        if self._thread_save and self._thread_save.is_alive():
            self._thread_save.join()

        if self._thread_proxieser and self._thread_proxieser.is_alive():
            self._thread_proxieser.join()

        if self._thread_monitor and self._thread_monitor.is_alive():
            self._thread_monitor.join()

        logging.info("ThreadPool has finished")

        return None

    ## ===================================================================================================================

    def get_thread_stop_flag(self):
        return self._thread_stop_flag

    def get_fetcher_number(self):
        return self._fetcher_number

    def get_number_dict(self, key=None):
        return self._number_dict[key] if key else self._number_dict

    def update_number_dict(self, key, value):
        self._lock.acquire()
        self._number_dict[key] += value
        self._lock.release()
        return None

    def is_all_tasks_done(self):
        return False if self._number_dict[TPEnum.TASKS_RUNNING] or self._number_dict[TPEnum.URL_FETCH_NOT] or \
                        self._number_dict[TPEnum.HTM_PARSE_NOT] or self._number_dict[TPEnum.ITEM_SAVE_NOT] else True

    ## ===================================================================================================================

    def add_a_task(self, task_name, task):

        if task_name == TPEnum.URL_FETCH and ((not self._url_filter) or self._url_filter.check_and_add(task[0])):
            self._queue_fetch.put_nowait(task)
            self.update_number_dict(TPEnum.URL_FETCH_NOT, +1)
            self.update_number_dict(TPEnum.COUNTER, +1)
        elif task_name == TPEnum.HTM_PARSE and self._thread_parse:
            self._queue_parse.put_nowait(task)
            self.update_number_dict(TPEnum.HTM_PARSE_NOT, +1)
        elif task_name == TPEnum.ITEM_SAVE and self._thread_save:
            self._queue_saver.put_nowait(task)
            self.update_number_dict(TPEnum.ITEM_SAVE_NOT, +1)
        elif (task_name == TPEnum.PROXIES) and self._thread_proxieser:
            self._queue_proxies.put_nowait(task)
            self.update_number_dict(TPEnum.PROXIES_LEFT, +1)
        return None

    def get_a_task(self, task_name):

        task = None
        if task_name == TPEnum.PROXIES:
            task = self._queue_proxies.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.PROXIES_LEFT, -1)
            return task
        if task_name == TPEnum.URL_FETCH:
            task = self._queue_fetch.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.URL_FETCH_NOT, -1)
        elif task_name == TPEnum.HTM_PARSE:
            task = self._queue_parse.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.HTM_PARSE_NOT, -1)
        elif task_name == TPEnum.ITEM_SAVE:
            task = self._queue_saver.get(block=True, timeout=10)
            self.update_number_dict(TPEnum.ITEM_SAVE_NOT, -1)
        self.update_number_dict(TPEnum.TASKS_RUNNING, +1)
        return task

    def finish_a_task(self, task_name):

        if task_name == TPEnum.PROXIES:
            self._queue_proxies.task_done()
            return
        if task_name == TPEnum.URL_FETCH:
            self._queue_fetch.task_done()
        elif task_name == TPEnum.HTM_PARSE:
            self._queue_parse.task_done()
        elif task_name == TPEnum.ITEM_SAVE:
            self._queue_saver.task_done()
        self.update_number_dict(TPEnum.TASKS_RUNNING, -1)
        return None

    ## ===================================================================================================================
