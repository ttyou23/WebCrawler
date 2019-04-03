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


def validUsefulProxy(proxy):
    """
    检验代理是否可用
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf8')
    proxies = {"http": "http://{proxy}".format(proxy=proxy)}
    try:
        # 超过20秒的代理就不要了
        r = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10, verify=False)
        print
        if r.status_code == 200 and r.json().get("origin"):
            # logger.info('%s is ok' % proxy)
            return True
    except Exception as e:
        print e
        # logger.error(e)
    return False


if __name__ == '__main__':
    print "====================================开始=========================================="
    logger = logging.getLogger()  # initialize logging class
    logger.setLevel(logging.DEBUG)  # default log level

    # for i in range(1):
    #     time.sleep(1)
    #     proxy_list = requests.get("http://192.168.59.130:8080/get_all/").content.split("\"")
    #     for proxy in proxy_list:
    #         if len(proxy) > 10:
    #             print proxy
    #     # print validUsefulProxy(proxy)

    # proxy = "121.69.37.6:9797"

    # # proxy = "43.249.226.65:53281"
    # print validUsefulProxy(proxy)

    try:
        # 超过20秒的代理就不要了
        proxies = {"http": "http://110.39.174.58:8080"}
        r = requests.get("http://dd.ma/iinW3M5C?invite_id=lalalalala", proxies=proxies, timeout=10, verify=False)
        print r.status_code
        if r.status_code == 200 and r.json().get("origin"):
            print r.status_code
            # logger.info('%s is ok' % proxy)
    except Exception as e:
        print e

    # proxy = "43.249.226.65:53281"
    # print validUsefulProxy(proxy)


    print "====================================结束=========================================="
    exit()

