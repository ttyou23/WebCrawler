# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 16:01
# @Author  : tianwei
# @Site    : 
# @File    : thread_fetch.py
# @Software: PyCharm

from thread_base import BaseThread, TPEnum


class FetchThread(BaseThread):
    """
    class of BaseThread, as base class of each thread
    """

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        BaseThread.__init__(name, worker, pool)
        return

    def working(self):
        """
        procedure of each thread, return True to continue, False to stop
        """
        url, func_callback, repeat = self._pool.get_a_task(TPEnum.URL_FETCH)

        state, result = self._worker.fetching(url, repeat)

        if state > 0:
            self._pool.add_a_task(TPEnum.HTM_PARSE, (url, func_callback, result))
            self._pool.update_number_dict(TPEnum.URL_FETCH_SUCC, +1)
        elif state == 0:
            self._pool.add_a_task(TPEnum.URL_FETCH, (func_callback, url, repeat + 1))
        else:
            self._pool.update_number_dict(TPEnum.URL_FETCH_FAIL, +1)
        return True
