# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 15:49
# @Author  : tianwei
# @Site    : 
# @File    : fulitxt.py
# @Software: PyCharm

import sys
import tools

reload(sys)
sys.setdefaultencoding("utf8")

ROOT_URL = "http://www.fltxt.com"

OUTFILE = "D:\\book\\fuli 20190516 "


def get_fuli_all(ori_url):
    content = tools.get_html_content_format_headers(ori_url, "body .nav a[class]")
    for item in content.items():
        url = item.attr.href
        print item.text(), url
        fuli_sort(url)
        break


def fuli_sort(ori_url):
    content = tools.get_html_content_format_headers(ori_url, "body .listBox")# .listBox a
    for item in content.items("ul a"):
        url = "%s%s" % (ROOT_URL, item.attr.href)
        print item.text(), url
    for item in content.items(".tspage a:contains('下一页')"):
        url = "%s%s" % (ROOT_URL, item.attr.href)
        print item.text(), url


if __name__ == '__main__':
    print "====================================begin============================================== "

    get_fuli_all(ROOT_URL)

    #测试

    print "====================================finish============================================== "
    exit(0)
