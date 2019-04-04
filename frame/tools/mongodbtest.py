# -*- coding: utf-8 -*-
# @Time    : 2019/3/29 10:38
# @Author  : tianwei
# @Site    : 
# @File    : mongodbtest.py
# @Software: PyCharm

import pymongo

if __name__ == '__main__':
    print "====================================开始=========================================="


    client = pymongo.MongoClient(host='192.168.59.139', port=27017)
    print "connect ok!"
    db = client.waf
    collection = db.runtest
    # student = {
    #     'id': '20170101',
    #     'name': 'Jordan',
    #     'age': 20,
    #     'gender': 'male'
    # }
    # result = collection.insert(student)
    # print(result)

    result = collection.find()
    print(type(result))
    print(result)

    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>结束>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    exit(0)