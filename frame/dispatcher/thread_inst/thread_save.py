# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 16:01
# @Author  : tianwei
# @Site    : 
# @File    : thread_save.py
# @Software: PyCharm

from thread_base import BaseThread, TPEnum


class SaveThread(BaseThread):
    """
    class of BaseThread, as base class of each thread
    """


    def working(self):
        """
        procedure of each thread, return True to continue, False to stop
        """
        url, save_list = self._pool.get_a_task(TPEnum.ITEM_SAVE)
        print url, save_list
        self._worker.saving(url, save_list)
        return True
