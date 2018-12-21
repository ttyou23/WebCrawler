# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 16:01
# @Author  : tianwei
# @Site    : 
# @File    : thread_parse.py
# @Software: PyCharm

from thread_base import BaseThread, TPEnum


class ParseThread(BaseThread):
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
        url, func_callback, result = self._pool.get_a_task(TPEnum.HTM_PARSE)

        state, url_list, save_list = self._worker.parsing(url, func_callback, result)

        if state > 0:
            if url_list and len(url_list) > 0:
                for url, func_callback in url_list:
                    self._pool.add_a_task(TPEnum.URL_FETCH, (url, func_callback, 0))
            if save_list and len(save_list) > 0:
                self._pool.add_a_task(TPEnum.ITEM_SAVE, (url, save_list))

        return True
