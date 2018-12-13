#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/31 14:16
# @Author  : tianwei
# @Site    : 
# @File    : fltxt_spider.py
# @Software: PyCharm

import re
from bs4 import BeautifulSoup
import requests
import sys;

reload(sys);
sys.setdefaultencoding("utf8")

FLTXT_HOME = "http://www.fltxt.com"

FLTXT_RECORD = "/txt/"
FLTXT_LIST = "index_"
FLTXT_BOOK = "/plus/download.php"
OUTPUT_FILE = "D:\\book\\fltxt.txt"
OUTTAG_FILE = "D:\\book\\fltxt_tag.txt"
OUTERROR_FILE = "D:\\book\\fltxt_errot.txt"

record_find_url_list = []


def write_book_url_file(book_url):
    with open(OUTPUT_FILE, 'a+') as f:
        f.write(book_url)


def write_book_tag(book_json):
    with open(OUTTAG_FILE, 'a+') as f:
        f.write(book_json)


def write_book_error(book_error):
    with open(OUTERROR_FILE, 'a+') as f:
        f.write(book_error)


def get_html_book_data(ori_url):
    book_link = ""
    book_file = ""
    try:
        # 获取网页内容
        s = requests.session()
        s.keep_alive = False
        response = requests.get(ori_url, headers={'Connection': 'close'})
        response.encoding = 'utf-8'
        data = response.text
        response.close();

        # 利用正则查找所有连接
        soup = BeautifulSoup(data, "html.parser")
        title = soup.find("a", attrs={"class": "downButton"})
        book_name = str(title.get('title'))
        book_name = book_name.replace("txt下载", "")
        book_link = title.get("href")

        title = soup.find("div", attrs={"class": "detail_right"})
        lis = title.find_all("li", attrs={"class": "small"})
        for li in lis:
            tempstring = str(li.get_text())
            if tempstring.startswith("小说作者："):
                book_auth = tempstring.replace("小说", "")

        book_file = "《" + book_name + "》（校对版全本）" + book_auth + ".txt"

        # link = FLTXT_HOME + data["location"].replace("&amp;", "&")
        filename = book_link[(book_link.rfind("/") + 1):book_link.rfind("?")]
        book_file = book_file + "\0" + filename
    except Exception, err:
        print 1, err
        write_book_error(ori_url + "\0" + str(err) + "\n")
    else:
        print "get_html_url: " + ori_url + "   -->ok"
    return book_link, book_file


def get_html_url(ori_url, tag, key, flag, index=0):
    link_list = []
    try:
        # 获取网页内容
        s = requests.session()
        s.keep_alive = False
        response = requests.get(ori_url, headers={'Connection': 'close'})
        response.encoding = 'utf-8'
        data = response.text
        response.close();

        # 利用正则查找所有连接
        title = BeautifulSoup(data, "html.parser").find_all(tag, attrs={key: flag})
        if len(title) > 0:
            content = title[index]
            link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", str(content))
    except Exception, err:
        print 2, err
        write_book_error(ori_url + "\0" + str(err) + "\n")
    else:
        print "get_html_url: " + ori_url + "   -->ok"
    return link_list


def get_fltxt_txt_book(ori_url):
    link, book_file = get_html_book_data(ori_url)
    if link is not None:
        # print(link)
        write_book_url_file(link + "\n")
    if book_file is not None:
        print(book_file)
        write_book_tag(book_file + "\n")


def get_fltxt_list(ori_url, dis_url):
    link_list = get_html_url(dis_url, "div", "class", "listBox")
    if link_list is None: return
    for url in link_list:
        urlstring = str(url)
        if urlstring is None: continue
        if urlstring.startswith(FLTXT_RECORD):
            subUrl = FLTXT_HOME + url
            # print(subUrl)
            get_fltxt_txt_book(subUrl)
            continue
        temp = ori_url + FLTXT_LIST
        subUrl = FLTXT_HOME + url
        if subUrl.startswith(temp):
            if subUrl not in record_find_url_list:
                record_find_url_list.append(subUrl)
                # print(subUrl)
                get_fltxt_list(ori_url, subUrl)


def get_fltxt_tag(ori_url):
    link_list = get_html_url(ori_url, "div", "class", "nav")
    if link_list is None: return
    for url in link_list:
        if url != ori_url:
            print(url)
            get_fltxt_list(url, url)


if __name__ == '__main__':
    print "====================================begin============================================== "
    get_fltxt_tag(FLTXT_HOME)

    # get_fltxt_list("http://www.fltxt.com/xuanhuan/", "http://www.fltxt.com/xuanhuan/index_2.html")

    # get_fltxt_txt_book("http://www.fltxt.com/txt/8371.html")
    print "====================================finish============================================== "
