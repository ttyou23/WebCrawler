# -*- coding: utf-8 -*-
# @Time    : 2019/5/16 10:59
# @Author  : tianwei
# @Site    : 
# @File    : zadzs.py
# @Software: PyCharm

import sys
import tools

reload(sys)
sys.setdefaultencoding("utf8")

ROOT_URL = "http://www.zadzs.com/"

OUTFILE = "D:\\book\\zadzs 20190516 "


def get_zadzs_all(ori_url):
    content = tools.get_html_content(ori_url, "body .g-bdw div[id=J_MM][class=m-menu] .sub")
    for item in content.items():
        title = item.find("h3").text()
        list_tag = item.find("a")
        for sub_item in list_tag.items():
            url = "%s%s" % (ROOT_URL, sub_item.attr.href)
            # print title, sub_item.text(), url
            zadzs_sort(url, url, title)
            break
        break


def zadzs_sort(ori_url, head_url, sort):
    print "zadzs_sort: ", ori_url
    content = tools.get_html_content(ori_url, "body .g-mnc")
    book_list = content.find("tbody tr div[class=book-name] a")
    for item in book_list.items():
        url = "%s%s" % (ROOT_URL, item.attr.href)
        # print "zadzs_sort: ", sort, item.text(), url
        zadzs_bookview(url, sort)
        break
    nexit_page = content.find("span[class=nums] a:contains('下一页')")
    for item in nexit_page.items():
        url = "%s%s" % (head_url, item.attr.href)
        # print url, item.text()
        zadzs_sort(url, head_url, sort)


def zadzs_bookview(ori_url, sort):
    content = tools.get_html_content(ori_url, "body div[class=ops] a")
    for item in content.items():
        url = "%s%s" % (ROOT_URL, item.attr.href)
        print "zadzs_rar: ", url, item.text()
        zadzs_download(url, sort)


def zadzs_download(ori_url, sort):
    content = tools.get_html_content(ori_url, "body .wrap .content")
    book_name = content.find("h2").text()
    for item in content.items("div[class='panel-body'] a:contains('TXT格式下载')"):
        url = "%s%s" % (ROOT_URL, item.attr.href)
        print "zadzs_download: ", url, item.text()
        zadzs_book_info(url, sort, book_name)


def zadzs_book_info(ori_url, sort, book_name):
    headers = tools.get_query_header(ori_url)
    link = headers["location"].replace("&amp;", "&")
    book_name = book_name + ".txt"#书籍名称
    file_name = link[(link.rfind("/")+1):len(link)]#下载的书籍文件名称

    tools.write_file("%s%s" % (ROOT_URL, link), "%s%s%s" % (OUTFILE, sort, ".txt"))
    tools.write_file(book_name + "\0" + file_name, "%s%s%s" % (OUTFILE, "flag", ".txt"))


if __name__ == '__main__':
    print "====================================begin============================================== "

    # get_zadzs_all(ROOT_URL)
    # get_zadzs_all(ROOT_URL)

    #测试
    # zadzs_sort("http://www.zxcs.me/sort/55")
    zadzs_download("http://www.zadzs.com//plus/download.php?open=0&aid=5398&cid=3", "")
    # zadzs_book_info("http://www.zadzs.com//plus/download.php?open=2&id=5398&uhash=6b1f5627f8065c19ee741071")

    print "====================================finish============================================== "
    exit(0)
