# coding:utf-8
import re
import threading
import time
import requests
from Queue import Queue
from threading import Thread
from bs4 import BeautifulSoup
import sys;
reload(sys);
sys.setdefaultencoding("utf8")

ZXCS8 = "http://www.spider.com/map.html"
ZXCS8_RECORD = "http://www.spider.com/record/"
ZXCS8_RECORD_OLD = "http://www.spider.com/record/201412"
ZXCS8_POST = "http://www.spider.com/post"
ZXCS8_DOWNLOAD = "http://www.spider.com/download.php"

print_log_lock = threading.Lock()
requests_lock = threading.Lock()
write_file_lock = threading.Lock()

def zxcs_print(log):
    print_log_lock.acquire()
    print log
    print_log_lock.release()

class BookSpider():

    def __init__(self ):
        self.record_find_url_list = []

    def set_filename(self, book_url):
        list_str = str(book_url).split("/")
        zxcs_print("D:\\book\\book" + str(list_str[len(list_str)-1]))
        self.book_filename = "D:\\book\\book" + str(list_str[len(list_str)-1])

    def test(self):
        time.sleep(3)
        zxcs_print("==================== test ==================================")


    def write_book_url_file(self, book_url):
        write_file_lock.acquire()
        with open(self.book_filename, 'a+') as f:
            f.write(book_url)
        write_file_lock.release()

    def get_html_book_data(self, ori_url):

        try:
            # 获取网页内容
            s = requests.session()
            s.keep_alive = False
            response = requests.get(ori_url)
            # response.encoding = 'utf-8'
            data = response.text
            response.close();

            # 利用正则查找所有连接
            title = BeautifulSoup(data, "html.parser").find('div', id='pleft')
            link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", str(title))
        except Exception, err:
            zxcs_print(err)
        else:
            zxcs_print("get_html_url: " + ori_url + "   -->ok")
        return link_list

    def get_html_url(self, ori_url):

        try:
            # 获取网页内容
            s = requests.session()
            s.keep_alive = False
            response = requests.get(ori_url)
            # response.encoding = 'utf-8'
            data = response.text
            response.close();

            # 利用正则查找所有连接
            link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", data)
        except Exception, err: print 1, err
        else:
            # print "get_html_url: " + ori_url + "   -->ok"
            return link_list

    def get_zxcs8_rar_book(self, ori_url):

        link_list = self.get_html_url(ori_url)
        if link_list == None:
            return
        for url in link_list:
            urlstring = str(url)
            if urlstring == None:
                continue

            if urlstring.endswith(".rar"):
                zxcs_print("rar url: " + url)
                self.write_book_url_file(url + "\r\n")


    def get_zxcs8_download(self, ori_url):

        link_list = self.get_html_url(ori_url)
        if link_list == None:
            return
        for url in link_list:
            urlstring = str(url)
            if urlstring == None or not urlstring.startswith(ZXCS8_DOWNLOAD):
                continue

            if not self.download_find_url_list.count(url):
                self.download_find_url_list.append(url)
                self.get_zxcs8_rar_book(url)

    def get_zxcs8_post(self, ori_url):

        zxcs_print("get_zxcs8_post url: " + ori_url)
        self.record_find_url_list.append(ori_url)
        link_list = self.get_html_book_data(ori_url)
        if link_list == None:
            return

        cout = 0
        for url in link_list:
            urlstring = str(url)
            if urlstring == None:
                continue

            if urlstring.startswith(ZXCS8_POST):
                if not self.post_find_url_list.count(url):
                    self.post_find_url_list.append(url)
                    self.get_zxcs8_download(url)
                    # cout = cout + 1
                    # if cout > 1:
                    #     break
                continue

            if urlstring.startswith(ZXCS8_RECORD):
                if not self.record_find_url_list.count(url):
                    zxcs_print("record url: " + url)
                    self.record_find_url_list.append(url)
                    self.get_zxcs8_post(url)

    # def get_zxcs8_record(self, ori_url):
    #
    #     link_list = self.get_html_url(ori_url)
    #     if link_list == None:
    #         return
    #
    #     cout = 0
    #     for url in link_list:
    #         urlstring = str(url)
    #         if urlstring == None:
    #             continue
    #
    #         if urlstring.startswith(ZXCS8_RECORD):
    #             if cmp(urlstring, ZXCS8_RECORD_OLD) < 0:
    #                 if not self.record_find_url_list.count(url):
    #                     print "record url: " + url
    #                     self.record_find_url_list.append(url)
    #                     self.get_zxcs8_post(url)
    #                     cout = cout + 1
    #                     # write_book_url_file(result_url_list)
    #                     print "result_url_list: " + str(len(self.result_url_list))
    #                     print "---------------cout: " + str(cout) + "-----------------------"



def get_zxcs8_record_url(ori_url):
    try:
        # 获取网页内容
        s = requests.session()
        s.keep_alive = False
        response = requests.get(ori_url)
        # response.encoding = 'utf-8'
        data = response.text
        response.close();

        # 利用正则查找所有连接
        link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", data)
    except Exception, err:
        print 1, err

    record_find_url_list = []

    if link_list == None:
        return record_find_url_list


    for url in link_list:
        urlstring = str(url)
        if urlstring == None:
            continue

        if urlstring.startswith(ZXCS8_RECORD):
            if cmp(urlstring, ZXCS8_RECORD_OLD) < 0:
                if not record_find_url_list.count(url):
                    print "record url: " + url
                    record_find_url_list.append(url)
    return record_find_url_list

class ThreadPoolManger():
    """线程池管理器"""

    def __init__(self, thread_num):
        # 初始化参数
        self.work_queue = Queue()
        self.thread_num = thread_num
        self.__init_threading_pool(self.thread_num)

    def __init_threading_pool(self, thread_num):
        # 初始化线程池，创建指定数量的线程池
        for i in range(thread_num):
            thread = ThreadManger(self.work_queue)
            thread.start()

    def add_job(self, ori_url):
        # 将任务放入队列，等待线程池阻塞读取，参数是被执行的函数和函数的参数
        self.work_queue.put((ori_url))

class ThreadManger(Thread):
    """定义线程类，继承threading.Thread"""

    def __init__(self, work_queue):
        Thread.__init__(self)
        self.work_queue = work_queue
        self.daemon = True
        self.books = BookSpider()

    def run(self):
        # 启动线程
        while True:
            ori_url = self.work_queue.get()
            self.books.set_filename(ori_url)
            # self.books.test()
            self.books.get_zxcs8_post(ori_url)
            self.work_queue.task_done()


if __name__=='__main__':

    zxcs_print(" ============================= BEGIN ============================")
    thread_pool = ThreadPoolManger(5)
    record_book_link = get_zxcs8_record_url(ZXCS8)
    for url in record_book_link:
        thread_pool.add_job(url)

    thread_pool.work_queue.join()
    zxcs_print("============================= FINISH ============================")
    zxcs_print("============================= FINISH ============================")
    zxcs_print("============================= FINISH ============================")