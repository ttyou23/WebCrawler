#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 17:05
# @Author  : tianwei
# @Site    : 爬取网页工具
# @File    : inst_fetch.py
# @Software: PyCharm


import time
import random
import logging
import requests


class Fetcher(object):
    """
    class of Fetcher, must include function working()
    """

    def __init__(self, max_repeat=3, sleep_time=0):
        """
        constructor
        :param max_repeat: default 3, maximum repeat count of a fetching
        :param sleep_time: default 0, sleeping time after a fetching
        """
        self._max_repeat = max_repeat
        self._sleep_time = sleep_time
        return

    def fetching(self, url, repeat):

        time.sleep(random.randint(0, self._sleep_time))
        try:
            fetch_state, fetch_result = self.url_fetch(url)
        except Exception as excep:
            if repeat >= self._max_repeat:
                fetch_state, fetch_result = -1, None
            else:
                fetch_state, fetch_result = 0, None

        logging.debug("%s end: fetch_state=%s, url=%s", self.__class__.__name__, fetch_state, url)
        return fetch_state, fetch_result

    def url_fetch(self, url):
        response = requests.get(url, params=None,  headers={'Connection':'close'}, data=None, timeout=(3.05, 10))
        response.encoding = "utf-8"
        result = (response.status_code, response.url, response.text)
        return 1, result
