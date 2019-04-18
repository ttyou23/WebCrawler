# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 10:44
# @Author  : tianwei
# @Site    : 
# @File    : format_file.py
# @Software: PyCharm

import sys;
reload(sys);
sys.setdefaultencoding("utf8")
import os

ROOT_FILE_PATH = u"D:\\dos\\新建文件夹\\"


def encode_file(fullpath, filepath, name):

    with open(fullpath, 'wb+') as fo:
        lenght = len(name)
        fo.seek(0, 0)
        read_data = fo.read(lenght)
        print read_data
        fo.write(name)
        fo.seek(0, 2)
        fo.write(read_data)
    pass


def decode_file(filepath):
    pass


def traversal_file(root_path):
    for dirpath, dirnames, filenames in os.walk(root_path):
        print filenames
        for filename in filenames:

            encode_file(os.path.join(dirpath, filename), dirpath, filename)
            print os.path.join(dirpath, filename)
        break
    pass
    pass


if __name__ == '__main__':
    print "====================================开始=========================================="

    traversal_file(ROOT_FILE_PATH)

    print "====================================结束=========================================="
    exit()