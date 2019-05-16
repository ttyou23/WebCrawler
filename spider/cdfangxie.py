# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 17:06
# @Author  : tianwei
# @Site    : 
# @File    : cdfangxie.py
# @Software: PyCharm

import sys
import tools

reload(sys)
sys.setdefaultencoding("utf8")

ROOT_URL = "http://www.cdfangxie.com"
OUTPUT_FILE = u"D:\\book\\房产预售\\房产信息表.xls"
OUTERROR_FILE = "D:\\book\\cdfangxie_error.txt"

HOUSE_TITLE = [u'区域', u'项目名称', u'项目咨询电话', u'预/现售证号', u'房屋用途', u'预售面积(平方米)', u'上市时间', u'购房登记规则下载地址', u'成品住房装修方案价格表下载地址', u'项目网址']


def get_cdfangxie_all(ori_url):
    content = tools.get_html_content_format_headers(ori_url, "body .nav a[class]")
    for item in content.items():
        url = item.attr.href
        print item.text(), url
        cdfangxie_sort(url)
        break


def cdfangxie_sort(ori_url):
    content = tools.get_html_content_format_headers(ori_url, "body .listBox")# .listBox a
    for item in content.items("ul a"):
        url = "%s%s" % (ROOT_URL, item.attr.href)
        print item.text(), url
    for item in content.items(".tspage a:contains('下一页')"):
        url = "%s%s" % (ROOT_URL, item.attr.href)
        print item.text(), url


if __name__ == '__main__':
    print "====================================begin============================================== "

    get_cdfangxie_all(ROOT_URL)

    #测试

    print "====================================finish============================================== "
    exit(0)
