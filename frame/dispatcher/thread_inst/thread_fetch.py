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

    def working(self):
        """
        procedure of each thread, return True to continue, False to stop
        """
        url, callback, repeat = self._pool.get_a_task(TPEnum.URL_FETCH)

        state, result = self._worker.fetching(url, repeat)

        if state > 0:
            self._pool.add_a_task(TPEnum.HTM_PARSE, (url, callback, result))
            self._pool.update_number_dict(TPEnum.URL_FETCH_SUCC, +1)
        elif state == 0:
            self._pool.add_a_task(TPEnum.URL_FETCH, (callback, url, repeat + 1))
        else:
            self._pool.update_number_dict(TPEnum.URL_FETCH_FAIL, +1)

        # ----*----
        while (self._pool.get_number_dict(TPEnum.HTM_PARSE_NOT) >= self._max_count) or (self._pool.get_number_dict(TPEnum.ITEM_SAVE_NOT) >= self._max_count):
            logging.debug("%s[%s] sleep 5 seconds because of too many 'HTM_PARSE_NOT' or 'ITEM_SAVE_NOT'", self.__class__.__name__, self.getName())
            time.sleep(5)

        return True
