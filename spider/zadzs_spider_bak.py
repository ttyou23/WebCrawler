#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/30 10:26
# @Author  : tianwei
# @Site    : 
# @File    : zadzs_spider_bak.py
# @Software: PyCharm

import re
from bs4 import BeautifulSoup
import requests
import sys;
reload(sys);
sys.setdefaultencoding("utf8")

ZADZS_HOME = "http://www.zadzs.com"
IDS_MALE = ["/male/dsgc/", "/male/xhxx/", "/male/khqh/", "/male/kbtl/", "/male/dmtr/", "/male/yxjj/", "/male/cyls/", "/male/jszz/"]
IDS_FEMALE = ["/female/xdyq/", "/female/gdyq/", "/female/xxmh/", "/female/dmbh/", "/female/khkb/", "/female/yltr/"]
ZADZS_LIST = "list"
ZADZS_RECORD = "/txt/"
ZADZS_BOOK = "/plus/download.php"
OUTPUT_FILE = "D:\\book\\zadzs.txt"

record_find_url_list = []

def write_book_url_file(book_url):
    with open(OUTPUT_FILE, 'a+') as f:
        f.write(book_url)

def get_html_book_data(ori_url):

    try:
        # 获取网页内容
        s = requests.session()
        s.keep_alive = False
        response = requests.get(ori_url, headers={'Connection':'close'})
        response.encoding = 'utf-8'
        data = response.text
        response.close();

        # 利用正则查找所有连接
        title = BeautifulSoup(data, "html.parser").find('div', attrs={'class':'g-mnc'})
        # title = BeautifulSoup(data, "html.parser").find('div', attrs={'class': 'g-mn'})
        # print(str(title))
        link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", str(title))
    except Exception, err:
        print 1, err
    else:
        print "get_html_url: " + ori_url + "   -->ok"
    return link_list

def get_html_url(ori_url):

    try:
        # 获取网页内容
        s = requests.session()
        s.keep_alive = False
        response = requests.get(ori_url, headers={'Connection':'close'})
        response.encoding = 'utf-8'
        data = response.text
        response.close();
        print(data)

        # 利用正则查找所有连接
        # title = BeautifulSoup(data, "html.parser").find('div', attrs={'class': 'm-bookdetail'})
        title = BeautifulSoup(data, "html.parser").find('div', attrs={'class': 'ops'})
        # print(str(title))
        link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", str(title))
    except Exception, err:
        print 1, err
    else:
        # print "get_html_url: " + ori_url + "   -->ok"
        return link_list


def get_zadzs_txt_book(ori_url):

    link_list = get_html_url(ori_url)
    if link_list == None: return
    for url in link_list:
        urlstring = str(url)
        if urlstring == None:continue

        if urlstring.startswith(ZADZS_BOOK):
            book_url = ZADZS_HOME + urlstring.replace("&amp;", "&")
            print book_url
            write_book_url_file(book_url + "\n")
            return


def get_zadzs_list(ori_url, dis_url):
    link_list = get_html_book_data(dis_url)
    if link_list == None: return
    for url in link_list:
        urlstring = str(url)
        if urlstring == None:continue
        if urlstring.startswith(ZADZS_RECORD):
            subUrl = ZADZS_HOME + url
            get_zadzs_txt_book(subUrl)
            continue
        if urlstring.startswith(ZADZS_LIST):
            if not url in record_find_url_list:
                record_find_url_list.append(url)
                subUrl = ori_url + url
                get_zadzs_list(ori_url, subUrl)


if __name__=='__main__':
    print "====================================begin============================================== "
    # for url_param in IDS_MALE:
    #     url = ZADZS_HOME + url_param
    #     get_zadzs_list(url, url)
    # for url_param in IDS_FEMALE:
    #     url = ZADZS_HOME + url_param
    #     get_zadzs_list(url, url)

    response = requests.head("http://www.zadzs.com/plus/download.php?open=2&id=3125&uhash=94bcb9804d23d63bcfcc1566", headers={'Connection':'close'})
    response.encoding = 'utf-8'
    data = response.headers
    response.close();
    print(data["location"])
    print "====================================finish============================================== "
