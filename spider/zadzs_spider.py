#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/31 14:16
# @Author  : tianwei
# @Site    : 
# @File    : zadzs_spider.py
# @Software: PyCharm

import re
from bs4 import BeautifulSoup
import requests
import sys;
reload(sys);
sys.setdefaultencoding("utf8")

ZADZS_HOME = "http://www.zadzs.com"
FLAG_MALE = "/male/"
FLAG_FEMALE = "/female/"
FLAG_BOOK = "/book/"
# IDS_MALE = ["/male/dsgc/", "/male/xhxx/", "/male/khqh/", "/male/kbtl/", "/male/dmtr/", "/male/yxjj/", "/male/cyls/", "/male/jszz/"]
# IDS_FEMALE = ["/female/xdyq/", "/female/gdyq/", "/female/xxmh/", "/female/dmbh/", "/female/khkb/", "/female/yltr/"]
ZADZS_LIST = "list"
ZADZS_RECORD = "/txt/"
ZADZS_BOOK = "/plus/download.php"
OUTPUT_FILE = "D:\\book\\zadzs.txt"
OUTTAG_FILE = "D:\\book\\zadzs_tag.txt"
OUTERROR_FILE = "D:\\book\\zadzs_errot.txt"

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
    link = ""
    book_file = ""
    try:
        # 获取网页内容
        s = requests.session()
        s.keep_alive = False
        response = requests.get(ori_url, headers={'Connection':'close'})
        response.encoding = 'utf-8'
        data = response.text
        response.close();

        # 利用正则查找所有连接
        title = BeautifulSoup(data, "html.parser").find_all("div", attrs={"class": "f-fl"})
        if len(title) > 3: content = title[3]
        else: content = title[0]
        book_name = content.h3.get('title')
        book_auth = content.h3.span.a.get_text()
        book_file = "《" + book_name + "》（校对版全本）作者：" + book_auth + ".txt"

        title = BeautifulSoup(data, "html.parser").find("div", attrs={"class": "ops"})
        sub_url = ZADZS_HOME + title.a.get("href")
        channel = title.a.get_text()

        # 获取网页内容
        s = requests.session()
        s.keep_alive = False
        response = requests.head(sub_url, headers={'Connection':'close'})
        response.encoding = 'utf-8'
        data = response.headers
        response.close();

        link = ZADZS_HOME + data["location"].replace("&amp;", "&")
        filename = link[(link.rfind("/")+1):len(link)]
        book_file = book_file + "\0" + filename + "\0" + channel
    except Exception, err:
        print 1, err
        write_book_error(ori_url + "\0" + err + "\n")
    else:
        print "get_html_url: " + ori_url + "   -->ok"
    return link, book_file


def get_html_url(ori_url, tag, key, flag, index=0):
    link_list=[]
    try:
        # 获取网页内容
        s = requests.session()
        s.keep_alive = False
        response = requests.get(ori_url, headers={'Connection':'close'})
        response.encoding = 'utf-8'
        data = response.text
        response.close();

        # 利用正则查找所有连接
        title = BeautifulSoup(data, "html.parser").find_all(tag, attrs={key: flag})
        # title = BeautifulSoup(data, "html.parser").find('div', attrs={'class': 'ops'})
        if len(title) > 0: content = title[index]
        else: content = title
        link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", str(content))
    except Exception, err:
        print 2, err
        write_book_error(ori_url + "\0" + err + "\n")
    else:
        print "get_html_url: " + ori_url + "   -->ok"
    return link_list


def get_zadzs_txt_book(ori_url):
    link, book_file = get_html_book_data(ori_url)
    if link is not None:
        write_book_url_file(link + "\n")
    if book_file is not None:
        write_book_tag(book_file + "\n")


def get_zadzs_list(ori_url, dis_url):
    link_list = get_html_url(dis_url, "div", "class", "g-mnc")
    if link_list == None: return
    for url in link_list:
        urlstring = str(url)
        if urlstring == None:continue
        if urlstring.startswith(ZADZS_RECORD):
            subUrl = ZADZS_HOME + url
            print(subUrl)
            get_zadzs_txt_book(subUrl)
            continue
        if urlstring.startswith(ZADZS_LIST):
            if url not in record_find_url_list:
                record_find_url_list.append(url)
                subUrl = ori_url + url
                print(subUrl)
                get_zadzs_list(ori_url, subUrl)


def get_zadzs_tag(ori_url):
    link_list = get_html_url(ori_url, "ul", "class", "f-cb", 1)
    if link_list == None: return
    for url in link_list:
        urlstring = str(url)
        if urlstring == None: continue
        subUrl = ZADZS_HOME + url
        if subUrl != ori_url:
            print(subUrl)
            # get_zadzs_list(subUrl, subUrl)
            break


if __name__=='__main__':
    print "====================================begin============================================== "
    # for url_param in IDS_MALE:
    #     url = ZADZS_HOME + url_param
    #     get_zadzs_list(url, url)
    # for url_param in IDS_FEMALE:
    #     url = ZADZS_HOME + url_param
    #     get_zadzs_list(url, url)

    # lines = get_zadzs_txt_book("http://www.zadzs.com/txt/2643.html")

    # link, book_file = get_html_book_data("http://www.zadzs.com/txt/3079.html")
    # print(link)
    # print(book_file)

    # get_zadzs_txt_book("http://www.zadzs.com/txt/789.html")

    OUTPUT_FILE = "D:\\book\\zadzs_book.txt"
    get_zadzs_tag(ZADZS_HOME + FLAG_BOOK)
    OUTPUT_FILE = "D:\\book\\zadzs_male.txt"
    get_zadzs_tag(ZADZS_HOME + FLAG_MALE)
    OUTPUT_FILE = "D:\\book\\zadzs_female.txt"
    get_zadzs_tag(ZADZS_HOME + FLAG_FEMALE)

    print "====================================finish============================================== "
