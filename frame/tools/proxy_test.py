# -*- coding: utf-8 -*-
# @Time    : 2019/2/17 16:42
# @Author  : tianwei
# @Site    : 
# @File    : proxy_test.py
# @Software: PyCharm
import json
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


    # {
    #     "access_token": "19_BXd7-VEPClL8hAPvOBHsoAtV7LrhQDIzTSe1UsvIN32gUlT8wGp03ugMvY-lKIPFHsyXO4zUj3dnKvAHVXfpSal63T4Cps_KtHRHdgcnEgX3JNuwVYogHrz46I0lSSCqPsi98DgCnC2faJMRZDFjACAOSU",
    #     "expires_in": 7200}

    # result = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxa4655c04a52ea238&secret=bfa0be03f8f53250214bf26fd0c327bb", timeout=10, verify=False)
    # print result.content

    # result = requests.get("https://api.weixin.qq.com/cgi-bin/template/get_all_private_template?access_token=19_BXd7-VEPClL8hAPvOBHsoAtV7LrhQDIzTSe1UsvIN32gUlT8wGp03ugMvY-lKIPFHsyXO4zUj3dnKvAHVXfpSal63T4Cps_KtHRHdgcnEgX3JNuwVYogHrz46I0lSSCqPsi98DgCnC2faJMRZDFjACAOSU")
    # print result.content

    # data = "{'access_token':'19_BXd7-VEPClL8hAPvOBHsoAtV7LrhQDIzTSe1UsvIN32gUlT8wGp03ugMvY-lKIPFHsyXO4zUj3dnKvAHVXfpSal63T4Cps_KtHRHdgcnEgX3JNuwVYogHrz46I0lSSCqPsi98DgCnC2faJMRZDFjACAOSU','expires_in':7200}"
    # print data
    # proxy = "43.249.226.65:53281"
    # proxy = "192.168.59.130:1080"
    # # validUsefulProxy(proxy)

    SEND_TEMPLATE_URL = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=ACCESS_TOKEN"
    ACCESS_TOKEN = "19_z6qsCNi-fFLlkLBX_ZuKN9BuaRm3ghtF5DzOuBm9qYvPjVzBfGHoai-fig-nA2Ohm6bwTNYrGE0qmxOGZNE93xaBXVg86mYL7jF-yPCRomrAJnYY-JHzp0MmcuiWpvnfHqEbS-V_6BXBsqvOEVSiAFAQHE"

    data = {}
    first = {}
    first["value"] = "测试测试"
    first["color"] = "#173177"
    keyword1 = {}
    keyword1["value"] = "2019年3月25号"
    keyword1["color"] = "#173177"
    keyword2 = {}
    keyword2["value"] = "消息通知"
    keyword2["color"] = "#173177"
    remark = {}
    remark["value"] = "网站www.scxjc.com在2018-12-12 13:46:34被用户xiaojincai进行了编辑修改，请予以关注！\r\n时间：xxxxxx\r\n某某某某公司"
    remark["color"] = "#173177"
    data["first"] = first
    data["keyword1"] = keyword1
    data["keyword2"] = keyword2
    data["remark"] = remark

    message = {}
    message["touser"] = "odPKSuKMD8I3OIbeVIn6cJfkvd5A"
    message["template_id"] = "Y5u8P8BzinJsM9CXFd8UeXSpxAucembJCNV3V33jHIk"
    message["data"] = data

    print message

    data_json = json.dumps(message)
    print data_json

    r = requests.post(SEND_TEMPLATE_URL.replace("ACCESS_TOKEN", ACCESS_TOKEN), data_json)
    print(r.content)


    print "====================================结束=========================================="
    exit()
