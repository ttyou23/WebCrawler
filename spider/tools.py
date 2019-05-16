#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/13 19:19
# @Author  : tianwei
# @Site    : 工具文件
# @File    : tools.py
# @Software: PyCharm

import os
import sys
import requests
import urllib2
import xlwt as xlwt
from pyquery import PyQuery

reload(sys)
sys.setdefaultencoding("utf8")

HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"}

def write_file(data, filepath=u"d://file.txt"):
    with open(filepath, 'a+') as f:
        f.write(data)


def read_file(data, filepath=u"d://file.txt"):
    with open(filepath, 'a+') as f:
        f.write(data)


def write_error(error, filepath=u"d://error.txt"):
    with open(filepath, 'a+') as f:
        f.write(error)


def save2excel(houses, filepath):
    """
    保存内容到xls里面
    :param houses: 房子预售信息
    :param filepath: 保存文件路径
    :return:
    """
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('info', cell_overwrite_ok=True)
    for i, row in enumerate(houses):
        for j, col in enumerate(row):
            booksheet.write(i, j, col)
    workbook.save(filepath)
    print os.getcwd()


def get_html_content(ori_url, selector):
    """
    获取网页标签中的内容
    :param ori_url:网址
    :param selector:内容过滤器
    :return: 获取内容
    """
    try:
        # 获取网页内容
        s = requests.session()
        s.keep_alive = False
        # response = requests.get(ori_url, headers={'Connection': 'close'})
        response = requests.get(ori_url, headers=HEADERS)
        response.encoding = "utf-8"
        data = response.text
        response.close()

        return PyQuery(data).find(selector)
    except Exception, err:
        print "error: ", err
        write_error(ori_url + "\0" + str(err) + "\n")
    return PyQuery("")


def get_html_content_format_headers(ori_url, selector):
    """
    获取网页标签中的内容
    :param ori_url:网址
    :param selector:内容过滤器
    :return: 获取内容
    """
    try:
        # 获取网页内容
        s = requests.session()
        s.keep_alive = False
        response = requests.get(ori_url, headers=HEADERS)
        response.encoding = "utf-8"
        data = response.text
        response.close()

        return PyQuery(data).find(selector)
    except Exception, err:
        print "error: ", err
        write_error(ori_url + "\0" + str(err) + "\n")
    return PyQuery("")


def get_query_header(ori_url):
    # 获取请求头
    s = requests.session()
    s.keep_alive = False
    response = requests.head(ori_url, headers=HEADERS)
    response.encoding = 'utf-8'
    data = response.headers
    response.close();
    return data
