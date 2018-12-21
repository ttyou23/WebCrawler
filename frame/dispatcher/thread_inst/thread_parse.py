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
        url, result = self._pool.get_a_task(TPEnum.HTM_PARSE)

        self._worker.working(url, result)
        return