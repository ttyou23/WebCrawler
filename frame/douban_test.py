# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 15:59
# @Author  : tianwei
# @Site    : 
# @File    : douban_test.py
# @Software: PyCharm

import logging

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
        print root_url
        url_list = []
        save_list = []
        status_code, url_now, html_text = content
        res_list = BeautifulSoup(html_text, "html.parser").find_all("a", class_="tag")
        for item in res_list:
            if len(item.get("class")) == 1:
                print "%s%s" % (root_url, item.get("href"))
                url_list.append(("%s%s" % (root_url, item.get("href")), self.htm_tag_parse))
                break

        return 1, url_list, save_list

    def htm_tag_parse(self, url, content):
        status_code, url_now, html_text = content
        res_list = BeautifulSoup(html_text, "html.parser").find_all("li", class_="subject-item")
        for item in res_list:
            book_name = item.find("h2").a.get("title")
            book_url = item.find("h2").a.get("href")
            book_pub = item.find("div", class_="pub")
            print book_name
            print book_url
            break
        url_list = []
        save_list = []
        return 1, url_list, save_list

    def htm_subject_parse(self, url, content):
        print url, content
        url_list = []
        save_list = []
        return 1, url_list, save_list


if __name__ == '__main__':
    print "====================================开始=========================================="
    logger = logging.getLogger()  # initialize logging class
    logger.setLevel(logging.DEBUG)  # default log level

    parser = MyParser()
    spider = WebSpider(parser)
    spider.start_working(root_url="https://book.douban.com/", fetcher_num=2)
    spider.wait_for_finish()

    print "====================================结束=========================================="
    exit()
