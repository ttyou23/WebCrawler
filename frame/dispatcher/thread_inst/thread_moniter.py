# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 14:12
# @Author  : tianwei
# @Site    : 
# @File    : thread_moniter.py
# @Software: PyCharm
import logging
import time

from thread_base import BaseThread, TPEnum


class MoniterThread(BaseThread):
    """
    class of BaseThread, as base class of each thread
    """

    def __init__(self, name, pool):
        """
        constructor of MonitorThread
        """
        BaseThread.__init__(self, name, None, pool)
        self._init_time = time.time()
        return

    def working(self):
        """
         monitor the thread pool, auto running, and return False if you need stop thread
         """
        time.sleep(5)
        info = "running_tasks=%s;" % self._pool.get_number_dict(TPEnum.TASKS_RUNNING)

        cur_fetch_not = self._pool.get_number_dict(TPEnum.URL_FETCH_NOT)
        cur_fetch_succ = self._pool.get_number_dict(TPEnum.URL_FETCH_SUCC)
        cur_fetch_fail = self._pool.get_number_dict(TPEnum.URL_FETCH_FAIL)
        info += " fetch:[NOT=%d, SUCC=%d, FAIL=%d];" % (cur_fetch_not, cur_fetch_succ, cur_fetch_fail)

        cur_parse_not = self._pool.get_number_dict(TPEnum.HTM_PARSE_NOT)
        cur_parse_succ = self._pool.get_number_dict(TPEnum.HTM_PARSE_SUCC)
        cur_parse_fail = self._pool.get_number_dict(TPEnum.HTM_PARSE_FAIL)
        info += " parse:[NOT=%d, SUCC=%d, FAIL=%d];" % (cur_parse_not, cur_parse_succ, cur_parse_fail)

        cur_save_not = self._pool.get_number_dict(TPEnum.ITEM_SAVE_NOT)
        cur_save_succ = self._pool.get_number_dict(TPEnum.ITEM_SAVE_SUCC)
        cur_save_fail = self._pool.get_number_dict(TPEnum.ITEM_SAVE_FAIL)
        info += " save:[NOT=%d, SUCC=%d, FAIL=%d];" % (cur_save_not, cur_save_succ, cur_save_fail)

        logging.info(info + " total_seconds=%d" % (time.time() - self._init_time))
        return not (self._pool.get_thread_stop_flag() and self._pool.is_all_tasks_done())
