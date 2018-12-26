# -*- coding: utf-8 -*-

import logging
import re
import time

import requests
import xlwt
from bs4 import BeautifulSoup
from dispatcher import *
from instances import *


class MySaver(Saver):

    def item_save(self, url, item):
        workbook = xlwt.Workbook(encoding='utf-8')
        booksheet = workbook.add_sheet('info', cell_overwrite_ok=True)
        for i, row in enumerate(item):
            for j, col in enumerate(row):
                booksheet.write(i, j, col)
        workbook.save("d://doubanbook.xls")
        return 1


class MyParser(Parser):

    def root_parse(self, root_url, content):
        url_list = []
        save_list = []
        status_code, url_now, html_text = content
        res_list = BeautifulSoup(html_text, "html.parser").find_all("a", text=re.compile(r"^20"))
        for item in res_list:
            print item.get("href")
            url_list.append((item.get("href"), self.htm_record_parse))
            break

        return 1, url_list, save_list

    def htm_record_parse(self, url, content):
        status_code, url_now, html_text = content
        url_list = []
        save_list = []
        res_list = BeautifulSoup(html_text, "html.parser").find_all("dl", attrs={"id": "plist"})
        for item in res_list:
            print item.dt.a.get("href")
            # save_list.append(book)
            url_list.append((item.dt.a.get("href"), self.htm_post_parse))

        return 1, url_list, save_list

    def htm_post_parse(self, url, content):
        status_code, url_now, html_text = content
        print url
        url_list = []
        save_list = []
        return 1, url_list, save_list

    def htm_download_parse(self, url, content):
        status_code, url_now, html_text = content
        print url
        url_list = []
        save_list = []
        return 1, url_list, save_list

def get_proxy():
    return requests.get("http://123.207.35.36:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

    # def freeProxyTwelve(page_count=2):
    #     """
    #     guobanjia http://ip.jiangxianli.com/?page=
    #     免费代理库
    #     超多量
    #     :return:
    #     """
    #     for i in range(1, page_count + 1):
    #         url = 'http://ip.jiangxianli.com/?page={}'.format(i)
    #         html_tree = getHtmlTree(url)
    #         tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
    #         if len(tr_list) == 0:
    #             continue
    #         for tr in tr_list:
    #             yield tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]

if __name__ == '__main__':
    print "====================================开始=========================================="

    # logger = logging.getLogger()  # initialize logging class
    # logger.setLevel(logging.DEBUG)  # default log level
    #
    # parser = MyParser()
    # saver = MySaver()
    # spider = WebSpider(parse_inst=parser, save_inst=saver, fetch_inst=None)
    # spider.start_working(root_url="http://www.zxcs.me/map.html", fetcher_num=1)
    # spider.wait_for_finish()
    response = requests.get("http://ip.jiangxianli.com/?page=1")
    response.encoding = "utf-8"
    body = BeautifulSoup(response.text, "html.parser").find_all("button", text=re.compile(r"^20"))
    proxy_list = body.find
    for proxy in proxy_list:
        # if type(proxy) = bs4.
        print proxy
    # print response.text
    # print get_proxy()
    print "====================================结束=========================================="
    exit()
