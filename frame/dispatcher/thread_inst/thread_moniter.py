# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 14:12
# @Author  : tianwei
# @Site    : 
# @File    : thread_moniter.py
# @Software: PyCharm

from thread_base import BaseThread, TPEnum

class MoniterThread(BaseThread):
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
        self._worker.working()
        return