# coding:utf-8
import sys
import tools

reload(sys)
sys.setdefaultencoding("utf8")

ZXCS8 = "http://www.zxcs.me/map.html"
ZXCS8_RECORD = "http://www.zxcs.me/record/"
ZXCS8_POST = "http://www.zxcs.me/post"
ZXCS8_DOWNLOAD = "http://www.zxcs.me/download.php"

ZXCS8_RECORD_UP = "http://www.zxcs.me/record/201906"
ZXCS8_RECORD_DOWN = "http://www.zxcs.me/record/201902"

post_find_url_list = []
record_find_url_list = []

OUTFILE = "D:\\book\\zxcs8 20181213.txt"
OUTFILE = "D:\\book\\zxcs8 20190212.txt"
OUTFILE = "D:\\book\\zxcs8 20190328.txt"
OUTFILE = "D:\\book\\zxcs8 20190508.txt"


def get_zxcs8_rar_book(ori_url):
    link_list = tools.get_html_url(ori_url, "span", "class", "downfile", 1)
    if link_list is None: return
    for url in link_list:
        urlstring = str(url)
        if urlstring is None: continue
        if urlstring.endswith(".rar"):
            print "rar url: " + url
            tools.write_file(url + "\n", OUTFILE)


def get_zxcs8_download(ori_url):
    link_list = tools.get_html_url(ori_url, "div", "class", "down_2", 0)
    if link_list is None: return
    for url in link_list:
        urlstring = str(url)
        if urlstring != None and urlstring.startswith(ZXCS8_DOWNLOAD):
            get_zxcs8_rar_book(url)


def get_zxcs8_post(ori_url):
    link_list = tools.get_html_url(ori_url, "div", "id", "pleft", 0)
    if link_list is None: return

    news_lines = []
    for line in link_list:
        if line not in news_lines:
            news_lines.append(line)

    for url in news_lines:
        url_string = str(url)
        if url_string is None: continue
        if url_string.startswith(ZXCS8_POST):
            get_zxcs8_download(url)
            continue
        if url_string.startswith(ZXCS8_RECORD):
            if url not in record_find_url_list:
                print "record url: " + url
                record_find_url_list.append(url)
                get_zxcs8_post(url)


def get_zxcs8_record(ori_url):
    link_list = tools.get_html_url(ori_url, "div", "id", "sort", 1)
    if link_list is None: return
    for url in link_list:
        url_string = str(url)
        if url_string is None: continue
        if url_string.startswith(ZXCS8_RECORD):
            if cmp(url_string, ZXCS8_RECORD_UP) <= 0 and cmp(url_string, ZXCS8_RECORD_DOWN) >= 0:
                if url not in record_find_url_list:
                    print "record url: " + url
                    record_find_url_list.append(url)
                    get_zxcs8_post(url)

def get_zxcs8_content(ori_url):
    link_list = tools.get_html_url(ori_url, "div", "id", "content")
    if link_list is None: return
    for url in link_list:
        url_string = str(url)
        if url_string is None: continue
        get_zxcs8_download(url)
        print url


if __name__ == '__main__':
    print "====================================begin============================================== "
    get_zxcs8_content(ZXCS8)

    print "====================================finish============================================== "
