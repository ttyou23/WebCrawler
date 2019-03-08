# -*- coding: utf-8 -*-
# @Time    : 2019/2/17 16:42
# @Author  : tianwei
# @Site    : 
# @File    : proxy_test.py
# @Software: PyCharm
import logging
logging.basicConfig()
import requests
from tread_tool import ThreadPoolManger


def validUsefulProxy(proxy, ):
    """
    检验代理是否可用
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf8')
    proxies = {"http": "http://{proxy}".format(proxy=proxy)}
    logger.info(proxies)
    try:
        # 超过20秒的代理就不要了
        r = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10, verify=False)
        if r.status_code == 200 :
            logger.info('%s is ===========okokokokok============' % proxy)
            return True
    except Exception as e:
        logger.error(e)
    return False


if __name__ == '__main__':
    print "====================================开始=========================================="
    logger = logging.getLogger()  # initialize logging class
    logger.setLevel(logging.DEBUG)  # default log level

    proxy = "121.69.37.6:9797"

    result = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx1045e227585f342b&secret=b447e5c66ee973bf76c426fc7713eb83", timeout=10, verify=False)
    print result.content

    # proxy = "43.249.226.65:53281"
    # proxy = "192.168.59.130:1080"
    # # validUsefulProxy(proxy)

    print "====================================结束=========================================="
    exit()
