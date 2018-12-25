# -*- coding: utf-8 -*-

import logging
import re

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
    return requests.get("http://127.0.0.1:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


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
    response = requests.get("http://www.zxcs.me/map.html", proxies={"http": "http://113.78.255.254:9000",})
    print response.text
    print "====================================结束=========================================="
    exit()
