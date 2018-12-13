#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/14 18:50
# @Author  : tianwei
# @Site    :
# @File    : thread_pool.py
# @Software: PyCharm

# 创建队列实例， 用于存储任务
import threading
import time
from Queue import Queue
from threading import Thread
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class ThreadInterface(object):
    def handle_job(self, agrs):
        print "handle job"

class ThreadPoolManger():
    """线程池管理器"""

    def __init__(self, thread_num):
        # 初始化参数
        self.work_queue = Queue()
        self.thread_num = thread_num
        self.http_request_lock = threading.Lock()
        self.write_file_lock = threading.Lock()
        self.__init_threading_pool(self.thread_num)

    def __init_threading_pool(self, thread_num):
        # 初始化线程池，创建指定数量的线程池
        for i in range(thread_num):
            thread = ThreadManger(self.work_queue, self.http_request_lock, self.write_file_lock)
            thread.start()

    def add_job(self, func, ori_url, file):
        # 将任务放入队列，等待线程池阻塞读取，参数是被执行的函数和函数的参数
        self.work_queue.put((func, ori_url, file))

class ThreadManger(Thread):
    """定义线程类，继承threading.Thread"""

    def __init__(self, work_queue, http_request_lock, write_file_lock):
        Thread.__init__(self)
        self.work_queue = work_queue
        self.daemon = True
        self.http_request_lock = http_request_lock
        self.write_file_lock = write_file_lock

    def run(self):
        # 启动线程
        while True:
            target, ori_url, file = self.work_queue.get()
            print "target(ori_url, file): " + str(ori_url) + file
            target(ori_url, file)
            self.work_queue.task_done()

def handle_request(ori_url, file):
    time.sleep(3)
    print "handle_request: " + str(ori_url) + file

if __name__=='__main__':
    thread_pool = ThreadPoolManger(4)
    for i in range(10):
        print i
        thread_pool.add_job(handle_request,  str(i) + "one", str(i) + "two")
    print " thread_pool.work_queue.join(): "
    thread_pool.work_queue.join()
    print "============================= END =============================: "