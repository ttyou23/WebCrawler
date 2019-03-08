# -*- coding: utf-8 -*-
# @Time    : 2019/2/17 16:46
# @Author  : tianwei
# @Site    : 
# @File    : tread_tool.py
# @Software: PyCharm

import sys
import threading
import time
from Queue import Queue
from threading import Thread
reload(sys)
sys.setdefaultencoding("utf-8")


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

    def add_job(self, func, param):
        # 将任务放入队列，等待线程池阻塞读取，参数是被执行的函数和函数的参数
        self.work_queue.put((func, param))


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
            func, param = self.work_queue.get()
            func(param)
            self.work_queue.task_done()