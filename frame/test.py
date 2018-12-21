# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 15:59
# @Author  : tianwei
# @Site    : 
# @File    : test.py
# @Software: PyCharm

from .dispatcher import *
from .instances import *
from tools import  *


class MyParser(Parser):

    def htm_parse(self, url, content):

        status_code, url_now, html_text = content

        url_list = []
        save_list = []

        # if (self._max_deep < 0) or (deep < self._max_deep):
        #     url_list = [(_url, keys, priority+1) for _url in re.findall(r"<a.+?href=\"(?P<url>.{5,}?)\".*?>", html_text, flags=re.IGNORECASE)]
        #
        # title = re.search(r"<title>(?P<title>.+?)</title>", html_text, flags=re.IGNORECASE)
        # save_list = [(url, title.group("title").strip(), datetime.datetime.now()), ] if title else []

        return 1, url_list, save_list

    def htm_tag_parse(self, url, content):
        return

    def htm_subject_parse(self, url, content):
        return


if __name__ == '__main__':
    print "====================================开始=========================================="

    parser = MyParser()
    spider = WebSpider(parser)
    print "====================================结束=========================================="
    exit()
