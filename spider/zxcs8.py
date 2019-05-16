# coding:utf-8
import sys
import tools

reload(sys)
sys.setdefaultencoding("utf8")

ROOT_URL = "http://www.zxcs.me/map.html"

OUTFILE = "D:\\book\\zxcs8 20181213.txt"
OUTFILE = "D:\\book\\zxcs8 20190212.txt"
OUTFILE = "D:\\book\\zxcs8 20190328.txt"
OUTFILE = "D:\\book\\zxcs8 20190516 "


def get_zxcs_all(ori_url):
    content = tools.get_html_content(ori_url, "body .wrap #sort ul li a:contains('(')")
    for item in content.items():
        url = item.attr.href
        zxcs_sort(url)


def get_zxcs_latest(ori_url):
    """
    下载最新书籍
    :param ori_url:
    :return:
    """
    content = tools.get_html_content(ori_url, ".wrap #content a")
    for item in content.items():
        url = item.attr.href
        zxcs_download(url)


def zxcs_sort(ori_url):
    content = tools.get_html_content(ori_url, "body .wrap #pleft")
    # 下载本页书籍
    book_sort = content.find("dl[id=plist] dt a")
    for item in book_sort.items():
        url = item.attr.href
        zxcs_download(url)

    #查找下一页链接
    flag = content.find("div[id=pagenavi] span").text()
    nexit_page = content.find("div[id=pagenavi] a:contains('" + str(int(flag) + 1) + "')")
    for item in nexit_page.items():
        url = item.attr.href
        zxcs_sort(url)


def zxcs_download(ori_url):
    content = tools.get_html_content(ori_url, "body .wrap #pleft .pagefujian .down_2 a")
    for item in content.items():
        url = item.attr.href
        text = item.text()
        print "zxcs_download: ", url, text
        zxcs_rar(url)


def zxcs_rar(ori_url):
    content = tools.get_html_content(ori_url, "body .wrap .content .downfile a")
    for item in content.items():
        url = item.attr.href
        text = item.text()
        print "zxcs_rar: ", url, text
        tools.write_file(url, "%s%s%s" % (OUTFILE, text, ".txt"))


if __name__ == '__main__':
    print "====================================begin============================================== "

    get_zxcs_latest(ROOT_URL)
    # get_zxcs_all(ROOT_URL)

    #测试
    # zxcs_sort("http://www.zxcs.me/sort/55")

    print "====================================finish============================================== "
    exit(0)
