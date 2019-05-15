# coding:utf-8
import sys
import tools

reload(sys)
sys.setdefaultencoding("utf8")

ROOT_URL = "http://www.zxcs.me/map.html"


def zxcs_get_all():

    # content = tools.get_html_content(ROOT_URL, "body .wrap #sort ul li a:contains('(')")
    content = tools.get_html_content(ROOT_URL, "body .wrap #sort ul li a:contains('(')")
    for a in content.items():
        print a.attr.href


if __name__ == '__main__':
    print "====================================begin============================================== "
    zxcs_get_all()

    print "====================================finish============================================== "
