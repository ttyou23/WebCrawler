# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 13:57
# @Author  : tianwei
# @Site    : 
# @File    : threads_pool.py
# @Software: PyCharm
import threading
from Queue import Queue

from .thread_inst import *
from instances import *


class ThreadPool(object):

    def __init__(self, parse_inst, fetch_inst=None, save_inst=None):

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

        self._fetch_queue = Queue()
        self._parse_queue = Queue()
        self._save_queue = Queue()

        self._fetch_inst = fetch_inst if fetch_inst else Fetcher()
        self._parse_inst = parse_inst
        self._save_inst = save_inst if save_inst else Saver()

        self._fetch_thread_list = []
        self._parse_thread = ParseThread("ParseThread", self._parse_inst, self)
        self._save_thread = SaveThread("SaveThread", self._save_inst, self)

        return

    ## ===================================================================================================================

    def start_working(self, root_url, fetcher_num):

        self._fetcher_number = fetcher_num
        self._thread_stop_flag = False

        self.add_a_task(TPEnum.URL_FETCH, (root_url, None, 0))

        self._fetch_thread_list = [FetchThread("FetchThread %d"%(i), self._fetch_inst, self) for i in xrange(fetcher_num)]

        for thread in self._fetch_thread_list:
            thread.setDaemon(True)
            thread.start()

        if self._parse_thread:
            self._parse_thread.setDaemon(True)
            self._parse_thread.start()

        if self._save_thread:
            self._save_thread.setDaemon(True)
        return

    def wait_for_finish(self):

        self._thread_stop_flag = True

        for thread in filter(lambda x:x.is_alive(), self._fetch_thread_list):
            thread.join()

        if self._parse_thread and self._parse_thread.is_alive():
            self._parse_thread.join()

        if self._save_thread and self._save_thread.is_alive():
            self._save_thread.join()

        return

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
        return

    def is_all_tasks_done(self):
        return False if self._number_dict[TPEnum.TASKS_RUNNING] or self._number_dict[TPEnum.URL_FETCH_NOT] or \
                        self._number_dict[TPEnum.HTM_PARSE_NOT] or self._number_dict[TPEnum.ITEM_SAVE_NOT] else True
    ## ===================================================================================================================

    def add_a_task(self, task_name, task):

        if task_name == TPEnum.URL_FETCH:
            self._fetch_queue.put_nowait(task)
            self.update_number_dict(TPEnum.URL_FETCH_NOT, +1)
            # self.update_number_dict(TPEnum.COUNTER, +1)
        elif task_name == TPEnum.HTM_PARSE:
            self._parse_queue.put_nowait(task)
            self.update_number_dict(TPEnum.HTM_PARSE_NOT, +1)
        elif task_name == TPEnum.ITEM_SAVE:
            self._save_queue.put_nowait(task)
            self.update_number_dict(TPEnum.ITEM_SAVE_NOT, +1)
        return

    def get_a_task(self, task_name):

        task = None
        if task_name == TPEnum.URL_FETCH:
            task = self._fetch_queue.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.URL_FETCH_NOT, -1)
            return task
        elif task_name == TPEnum.HTM_PARSE:
            task = self._parse_queue.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.HTM_PARSE_NOT, -1)
            return task
        elif task_name == TPEnum.ITEM_SAVE:
            task = self._save_queue.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.ITEM_SAVE_NOT, -1)
            return task
        self.update_number_dict(TPEnum.TASKS_RUNNING, +1)
        return task

    def finish_a_task(self, task_name):
        if task_name == TPEnum.URL_FETCH:
            self._fetch_queue.task_done()
        elif task_name == TPEnum.HTM_PARSE:
            self._parse_queue.task_done()
        elif task_name == TPEnum.ITEM_SAVE:
            self._save_queue.task_done()
        self.update_number_dict(TPEnum.TASKS_RUNNING, -1)
        return

    ## ===================================================================================================================
