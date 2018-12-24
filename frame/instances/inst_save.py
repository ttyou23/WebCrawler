#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 17:06
# @Author  : tianwei
# @Site    : 保存数据
# @File    : inst_save.py
# @Software: PyCharm


import sys
import logging


class Saver(object):
    """
    class of Saver, must include function working()
    """

    def __init__(self, save_pipe=sys.stdout):
        self._save_pipe = save_pipe
        return

    def saving(self, url, item):

        try:
            save_state = self.item_save(url, item)
        except Exception as excep:
            logging.error("%s error: excep=%s", self.__class__.__name__, excep)
            save_state = -1

        logging.debug("%s end: save_state=%s, url=%s", self.__class__.__name__, save_state, url)
        return save_state

    def item_save(self, url, item):
        """
        save the item of a url, you can rewrite this function, parameters and returns refer to self.working()
        """
        with open("d:\\file.txt", 'a+') as f:
            for temp in item:
                data = "".join(str(col) for col in temp)
                f.write(data.encode('gbk'))
        return 1