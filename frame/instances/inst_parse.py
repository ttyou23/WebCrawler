#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 17:06
# @Author  : tianwei
# @Site    : 解析网页
# @File    : inst_parse.py
# @Software: PyCharm


import re
import logging
import datetime


class Parser(object):
    """
    class of Parser, must include function working()
    """

    def __init__(self, max_deep=0):
        """
        constructor
        :param max_deep: default 0, if -1, spider will not stop until all urls are fetched
        """
        self._max_deep = max_deep
        return

    def parsing(self, url, content, func_callback=None):

        try:
            if not func_callback:
                parse_state, url_list, save_list = self.htm_parse(url, content)
            else:
                parse_state, url_list, save_list = func_callback(url, content)
        except Exception as excep:
            parse_state, url_list, save_list = -1, [], []

        return parse_state, url_list, save_list

    def htm_parse(self, url, content):

        status_code, url_now, html_text = content

        # url_list = []
        # if (self._max_deep < 0) or (deep < self._max_deep):
        #     url_list = [(_url, keys, priority+1) for _url in re.findall(r"<a.+?href=\"(?P<url>.{5,}?)\".*?>", html_text, flags=re.IGNORECASE)]
        #
        # title = re.search(r"<title>(?P<title>.+?)</title>", html_text, flags=re.IGNORECASE)
        # save_list = [(url, title.group("title").strip(), datetime.datetime.now()), ] if title else []
        url_list = []
        save_list = []
        return 1, url_list, save_list
