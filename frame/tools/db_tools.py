# # -*- coding: utf-8 -*-
# # @Time    : 2018/12/26 13:50
# # @Author  : tianwei
# # @Site    :
# # @File    : db_tools.py
# # @Software: PyCharm
#
#
# import MySQLdb
# import sys
#
# reload(sys)
# sys.setdefaultencoding("utf-8")
#
# ############################################# 配置 begin #########################################
#
# # #数据库连接配置
# # MYSQL_HOSTS = '10.4.5.223'
# # MYSQL_USER = 'root'
# # MYSQL_PASSWORD = 'Abc123456..'
# # MYSQL_PORT = '3306'
# # MYSQL_DB = 'config_manager'
#
#
# # #数据库连接配置
# # MYSQL_HOSTS = '10.10.200.250'
# # MYSQL_USER = 'test'
# # MYSQL_PASSWORD = '123asd'
# # MYSQL_PORT = '3306'
# # MYSQL_DB = 'config_manager'
#
# # 数据库连接配置
# MYSQL_HOSTS = '192.168.59.134'
# MYSQL_PORT = 3306
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = '123asd'
# MYSQL_DB = 'webcrawler'
#
# # 待测试的域名存放位置
# WAF_URL_FILE = 'e:\\URL.txt'
# # CDN的IP
# WAF_CDN_IP = '10.4.5.231'
# # 测试结果存放的文件夹
# WAF_HOSTS_FILE = 'e:\\WAF_HOSTS.txt'
#
#
# ############################################# 配置 end #########################################
#
# class WebCrawlerDb(object):
#
#     def db_connect(self):
#         self.db = MySQLdb.connect(MYSQL_HOSTS, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, charset='utf8')
#
#     def create_proxy_table(self):
#         # 使用cursor()方法获取操作游标
#         cursor = self.db.cursor()
#
#         # 如果数据表已经存在使用 execute() 方法删除表。
#         cursor.execute("DROP TABLE IF EXISTS proxy")
#
#         # 创建数据表SQL语句
#         sql = """CREATE TABLE proxy (
#                  id int primary key,
#                  proxy   CHAR(64) NOT NULL,
#                  type  INT NOT NULL,
#                  LAST_NAME  CHAR(20),
#                  AGE INT,
#                  SEX CHAR(1),
#                  INCOME FLOAT )"""
#
#         return cursor.execute(sql)
#
#     def insert_proxy(self):
#         return
#
#     def update_proxy(self):
#         return
#
#     def get_proxy(self):
#         sql = 'SELECT domain FROM website  ORDER BY id'
#
#         try:
#             cursor = self.db.cursor()
#             # 执行SQL语句
#             cursor.execute(sql)
#             # 获取所有记录列表
#             results = cursor.fetchall()
#             print results
#             hosts_lines = []
#             url_lines = []
#             for row in results:
#                 domain = row[0]
#                 # scheme = row[1]
#                 hosts_lines.append(WAF_CDN_IP + ' ' + str(domain).replace('@.', '') + '\r\n')
#                 # url_lines.append(scheme + '://' + str(domain).replace('@.', '') + '\r\n')
#                 # 打印结果
#                 print domain
#
#             # write_file(WAF_URL_FILE, url_lines)
#             # write_file(WAF_HOSTS_FILE, hosts_lines)
#         except:
#             print "Error: unable to fecth data"
#         return
#
#     def db_close(self):
#         # 关闭数据库连接
#         self.db.close()
#
#
# def write_file(path, lines):
#     with open(path, 'w') as f:
#         f.writelines(lines)
#
#
# if __name__ == '__main__':
#     web_db = WebCrawlerDb()
#     web_db.db_connect()
#     print web_db.create_table()
