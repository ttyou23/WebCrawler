# -*- coding: utf-8 -*-
# @Time    : 2018/12/27 15:05
# @Author  : tianwei
# @Site    : 
# @File    : test_proxy.py
# @Software: PyCharm
import logging
import time
import requests



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
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
        if r.status_code == 200 and r.json().get("origin"):
            logger.info('%s is ok' % proxy)
            return True
    except Exception as e:
        print e
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
        # print validUsefulProxy(proxy)


    try:
        # 超过20秒的代理就不要了
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
        if r.status_code == 200 and r.json().get("origin"):
            logger.info('%s is ok' % proxy)
    except Exception as e:
        print e

    # proxy = "81.33.4.214:61711"
    # # proxy = "43.249.226.65:53281"
    # print validUsefulProxy(proxy)

    print "====================================结束=========================================="
    exit()
