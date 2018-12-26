# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 16:01
# @Author  : tianwei
# @Site    : 
# @File    : thread_parse.py
# @Software: PyCharm
import logging

from thread_base import BaseThread, TPEnum


class ParseThread(BaseThread):
    """
    class of BaseThread, as base class of each thread
    """

    def working(self):
        """
        procedure of each thread, return True to continue, False to stop
        """
        counter, url, callback, result = self._pool.get_a_task(TPEnum.HTM_PARSE)

        state, url_list, save_list = self._worker.parsing(url, callback, result)
        logging.debug("%s  state=%d  url_list=%d  save_list=%d, url=%s", self.__class__.__name__, state, len(url_list), len(save_list), url)

        if state > 0:
            self._pool.update_number_dict(TPEnum.HTM_PARSE_SUCC, +1)
            if url_list and len(url_list) > 0:
                for url, callback in url_list:
                    self._pool.add_a_task(TPEnum.URL_FETCH, (counter, url, callback, 0))
            if save_list and len(save_list) > 0:
                self._pool.add_a_task(TPEnum.ITEM_SAVE, (url, save_list))
        else:
            self._pool.update_number_dict(TPEnum.HTM_PARSE_FAIL, +1)

        self._pool.finish_a_task(TPEnum.HTM_PARSE)

        return True
