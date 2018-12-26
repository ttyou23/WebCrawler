# _*_ coding: utf-8 _*_

"""
inst_proxies.py by xianhu
"""

import time
import logging

import requests


class Proxieser(object):
    """
    class of Proxieser, must include function working()
    """

    def __init__(self, sleep_time=1):
        """
        constructor
        :param sleep_time: default 10, sleeping time after a fetching
        """
        self._sleep_time = sleep_time
        return

    def working(self):
        """
        working function, must "try, except" and don't change the parameters and returns
        :return proxies_state: can be -1(get failed), 1(get success)
        :return proxies_list: [{"http": "http://auth@ip:port", "https": "https://auth@ip:port"}, ...]
        """
        logging.debug("%s start", self.__class__.__name__)

        # time.sleep(self._sleep_time)
        try:
            proxies_state, proxy = self.proxies_get()
        except Exception as excep:
            proxies_state, proxy = -1, None
            logging.error("%s error: %s", self.__class__.__name__, excep)

        logging.debug("%s end: proxies_state=%s, proxies=%s", self.__class__.__name__, proxies_state, proxy)
        return proxies_state, proxy

    def proxies_get(self):
        proxy = requests.get("http://123.207.35.36:5010/get/").content
        return 1, {"http": "http://{}".format(proxy)}
