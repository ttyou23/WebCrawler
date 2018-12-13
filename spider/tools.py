#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/13 19:19
# @Author  : tianwei
# @Site    : 工具文件
# @File    : tools.py
# @Software: PyCharm

import os
import sys
reload(sys)
sys.setdefaultencoding("utf8")

import re
from bs4 import BeautifulSoup
import requests
import xlwt as xlwt


def write_error(book_error, filepath=u"d://error.txt"):
    with open(filepath, 'a+') as f:
        f.write(book_error)

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

def get_html_content(ori_url, tag, key, flag):
    """
    获取网页标签中的内容
    :param ori_url:网址
    :param tag:标签
    :param key:
    :param flag:
    :return: 标签内容列表
    """
    try:
        # 获取网页内容
        s = requests.session()
        s.keep_alive = False
        response = requests.get(ori_url, headers={'Connection':'close'})
        response.encoding = 'utf-8'
        data = response.text
        response.close();

        res_set = BeautifulSoup(data, "html.parser").find_all(tag, attrs={key: flag})
        return res_set
    except Exception, err:
        print 2, err
        write_error(ori_url + "\0" + str(err) + "\n")
    else:
        print "get_html_conten: " + ori_url + "   -->ok"
    return ""


def get_html_url(ori_url, tag, key, flag, index=0):
    """
    获取网页指定标签中所有链接
    :param ori_url:网址
    :param tag:标签名
    :param key:
    :param flag:
    :param index:
    :return: 所有链接列表
    """
    link_list = []
    try:
        # 获取网页内容
        s = requests.session()
        s.keep_alive = False
        response = requests.get(ori_url, headers={'Connection':'close'})
        response.encoding = 'utf-8'
        data = response.text
        response.close();

        # 利用正则查找所有连接
        res_set = BeautifulSoup(data, "html.parser").find_all(tag, attrs={key: flag})
        if res_set and len(res_set)>0:
            content = res_set[index]
        else : content = res_set
        link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", str(content))
    except Exception, err:
        print 2, err
        write_error(ori_url + "\0" + str(err) + "\n")
    else:
        print "get_html_url: " + ori_url + "   -->ok"
    return link_list
