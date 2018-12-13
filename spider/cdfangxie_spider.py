#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/12 16:30
# @Author  : tianwei
# @Site    : 爬取成都房协网发布信息
# @File    : cdfangxie_spider.py
# @Software: PyCharm
import os
import sys;
reload(sys);
sys.setdefaultencoding("utf8")

import re
from bs4 import BeautifulSoup
import requests
import xlwt as xlwt


CDFANGXIE = "http://www.cdfangxie.com"
OUTPUT_FILE = u"D:\\book\\房产预售\\房产信息表.xls"
OUTERROR_FILE = "D:\\book\\cdfangxie_error.txt"

HOUSE_TITLE = [u'区域', u'项目名称', u'项目咨询电话', u'预/现售证号', u'房屋用途', u'预售面积(平方米)', u'上市时间', u'购房登记规则下载地址', u'成品住房装修方案价格表下载地址', u'项目网址']

def write_error(book_error):
    with open(OUTERROR_FILE, 'a+') as f:
        f.write(book_error)

def save2memory(houses, file):
    """
    保存内容到xls里面
    :param en_cn_map:  英文中文对应字典 {"name": "名字"}, OrderedDict
    :param content:
    :return:
    """
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('info', cell_overwrite_ok=True)
    for i, row in enumerate(houses):
        for j, col in enumerate(row):
            booksheet.write(i, j, col)
    workbook.save(file)
    print os.getcwd()

def get_html_data(ori_url, tag, key, flag):
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
        return res_set
    except Exception, err:
        print 2, err
        write_error(ori_url + "\0" + str(err) + "\n")
    else:
        print "get_html_url: " + ori_url + "   -->ok"
    return ""


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
        res_set = BeautifulSoup(data, "html.parser").find_all(tag, attrs={key: flag})
        if res_set and len(res_set)>0:
            content = res_set[index]
        else: content = res_set
        link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", str(content))
    except Exception, err:
        print 2, err
        write_error(ori_url + "\0" + str(err) + "\n")
    else:
        print "get_html_url: " + ori_url + "   -->ok"
    return link_list

def get_fangxie_info(url_json):
    print url_json

    content = get_html_data(url_json["ori_url"], "div", "class", "infor")
    if content and len(content)>0:
        p_list = content[0].find_all("p")
        if p_list and len(p_list)>0:
            for item in p_list:
                span = item.span
                if not span.text:
                    continue
                data = str(span.text)
                print data
                if data.startswith(u"项目咨询电话:"):
                    url_json["phone"] = data.split(u":")[1]
                elif data.startswith(u"预/现售证号:"):
                    url_json["sale"] = data.split(":")[1]
                elif data.startswith(u"房屋用途:"):
                    url_json["usage"] = data.split(u":")[1]
                elif data.startswith(u"预售面积(平方米):"):
                    url_json["area"] = data.split(u":")[1]
                elif data.startswith(u"上市时间:"):
                    url_json["date"] = data.split(u":")[1]
                elif data.startswith(u"购房登记规则点击下载"):
                    try:
                        url_json["url_reg"] = span.span.a["href"]
                    except Exception, err:
                        print err
                elif data.startswith(u"成品住房装修方案价格表点击下载"):
                    try:
                        url_json["url_house"] = span.span.a["href"]
                    except Exception, err:
                        print err

            house = []
            house.append(url_json.get("zone", " "))
            house.append(url_json.get("name", " "))
            house.append(url_json.get("phone", " "))
            house.append(url_json.get("sale", " "))
            house.append(url_json.get("usage", " "))
            house.append(url_json.get("area", " "))
            house.append(url_json.get("date", " "))
            house.append(url_json.get("url_reg", " "))
            house.append(url_json.get("url_house", " "))
            house.append(url_json.get("ori_url", " "))
            print url_json
            return house
    return ""


def get_fangxie_list(ori_url):
    house_list = []
    print "get_fangxie_list: %s"%ori_url
    content = get_html_data(ori_url, "div", "class", "right_cont")
    if content:
        #获取房产信息列表
        ul_list = content[0].ul.contents
        for item in ul_list:
            if item.span:
                url_json = {}
                url_json["ori_url"] = "%s%s"%(CDFANGXIE, item.span.a.get("href"))
                zone = item.span.a.get("title").split("|");
                url_json["zone"] = zone[0]
                url_json["name"] = zone[1]
                house = get_fangxie_info(url_json)
                if house and len(house)>0:
                    house_list.append(house)
                    break
        #获取下一页链接
        page_list = content[0].div.b
        if page_list:
            for item in page_list:
                if type(item) == type(content[0]) and item.text == u"下一页":
                    pass
                    # next_house_list = get_fangxie_list("%s%s"%(CDFANGXIE, item["href"]))
                    # if next_house_list and len(next_house_list) > 0:
                    #     house_list.extend(next_house_list)
                    #     break
    return house_list


def get_fangxie_tab(ori_url):
    url_list = get_html_url(ori_url, "div", "class", "cont1_rukou", index=0)
    if url_list and len(url_list)>0:
        print "%s%s"%(CDFANGXIE, url_list[0])
        total_houses = []
        total_houses.append(HOUSE_TITLE)
        houses = get_fangxie_list("%s%s"%(CDFANGXIE, url_list[0]))
        total_houses.extend(houses)
        save2memory(total_houses, OUTPUT_FILE)


if __name__=='__main__':

    print "====================================begin============================================== "
    get_fangxie_tab(CDFANGXIE)
    print "====================================finish============================================== "