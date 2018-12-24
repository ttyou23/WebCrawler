# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 16:01
# @Author  : tianwei
# @Site    : 
# @File    : thread_save.py
# @Software: PyCharm
import logging

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
        state = self._worker.saving(url, save_list)
        logging.debug("%s  state=%d  url=%s", self.__class__.__name__, state,  url)
        if state > 0:
            self._pool.update_number_dict(TPEnum.ITEM_SAVE_SUCC, +1)
        else:
            self._pool.update_number_dict(TPEnum.ITEM_SAVE_FAIL, +1)
        return True
