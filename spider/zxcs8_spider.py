# coding:utf-8
import re
from bs4 import BeautifulSoup
import requests
import sys;
reload(sys);
sys.setdefaultencoding("utf8")

ZXCS8 = "http://www.spider.com/map.html"
ZXCS8_RECORD = "http://www.spider.com/record/"
ZXCS8_POST = "http://www.spider.com/post"
ZXCS8_DOWNLOAD = "http://www.spider.com/download.php"

ZXCS8_RECORD_UP   = "http://www.spider.com/record/201808"
ZXCS8_RECORD_DOWN = "http://www.spider.com/record/201808"

ZXCS8_ID = "id"
ZXCS8_CLASS = "class"
ZXCS8_FLAG_POST = "pleft"
ZXCS8_FLAG_DOWNLOAD = "down_2"
ZXCS8_FLAG_BOOK = "downfile"
ZXCS8_DOWNLOAD_LINE_1 = "线路一"

result_url_list = []
record_find_url_list = []

def write_book_url_file(book_url):
    with open('D:\\book\\spider.txt', 'a+') as f:
        f.write(book_url)

def get_html_book_data(url):
    link_list = []
    try:
        # 获取网页内容
        s = requests.session()
        s.keep_alive = False
        response = requests.get(url, headers={'Connection':'close'})
        response.encoding = 'utf-8'
        data = response.text
        response.close();

        # 利用正则查找所有连接
        title = BeautifulSoup(data, "html.parser").find('span', attrs={'class': 'downfile'})
        print(str(title))
        link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", str(title))
    except Exception, err:
        print 1, err
    else:
        print "get_html_url: " + url + "   -->ok"
    return link_list


def get_html_url(url, key, flag):
    link_list = []
    try:
        # 获取网页内容
        s = requests.session()
        s.keep_alive = False
        response = requests.get(url, headers={'Connection':'close'})
        response.encoding = 'utf-8'
        data = response.text
        response.close();

        # 利用正则查找所有连接
        title = BeautifulSoup(data, "html.parser").find('div', attrs={key: flag})
        print(str(title))
        link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", str(title))
    except Exception, err:
        print 1, err
    else:
        print "get_html_url: " + url + "   -->ok"
    return link_list

def get_zxcs8_rar_book(ori_url):

    link_list = get_html_book_data(ori_url)
    if link_list == None:
        return
    for url in link_list:
        urlstring = str(url)
        if urlstring == None:
            continue

        if urlstring.endswith(".rar"):
            print "rar url: " + url
            result_url_list.append(url + "\r\n")
            write_book_url_file(url + "\r\n")


def get_zxcs8_download(ori_url):
    link_list = get_html_url(ori_url, ZXCS8_CLASS, ZXCS8_FLAG_DOWNLOAD)
    if link_list == None:
        return
    for url in link_list:
        urlstring = str(url)
        if urlstring != None and urlstring.startswith(ZXCS8_DOWNLOAD):
            get_zxcs8_rar_book(url)

def get_zxcs8_post(ori_url):
    link_list = get_html_url(ori_url, ZXCS8_ID, ZXCS8_FLAG_POST)
    if link_list == None:
        return
    for url in link_list:
        urlstring = str(url)
        if urlstring == None:
            continue
        if urlstring.startswith(ZXCS8_POST):
            get_zxcs8_download(url)
            continue
        if urlstring.startswith(ZXCS8_RECORD):
            if not url in record_find_url_list:
                print "record url: " + url
                record_find_url_list.append(url)
                get_zxcs8_post(url)


def get_zxcs8_record(ori_url):

    link_list = get_html_url(ori_url, "", "")
    if link_list == None:
        return

    cout = 0
    for url in link_list:
        urlstring = str(url)
        if urlstring == None:
            continue

        if urlstring.startswith(ZXCS8_RECORD):
            if cmp(urlstring, ZXCS8_RECORD_UP) <= 0 and cmp(urlstring, ZXCS8_RECORD_DOWN) >= 0:
                if not url in record_find_url_list:
                    print "record url: " + url
                    record_find_url_list.append(url)
                    get_zxcs8_post(url)
                    cout = cout + 1
                    print "result_url_list: " + str(len(result_url_list))
                    print "------------------------------------cout: " + str(cout) + "-----------------------------------------------"


if __name__=='__main__':

    print "====================================begin============================================== "
    get_zxcs8_record(ZXCS8)
    # with open('D:\\book\\spider.txt', 'a+') as f:
    #     f.writelines(result_url_list)
    #     f.flush()
    #
    # list = get_html_book_data("http://www.zxcs8.com/download.php?id=2790")
    # for url in list:
    #     print(url)
    print "====================================finish============================================== "

