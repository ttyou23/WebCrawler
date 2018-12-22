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

    def parsing(self, url, callback, content):

        try:
            if not callback:
                parse_state, url_list, save_list = self.root_parse(url, content)
            else:
                parse_state, url_list, save_list = callback(url, content)
        except Exception as excep:
            parse_state, url_list, save_list = -1, [], []

        return parse_state, url_list, save_list

    def root_parse(self, root_url, content):

        status_code, url_now, html_text = content
        url_list = []
        save_list = []
        return 1, url_list, save_list
