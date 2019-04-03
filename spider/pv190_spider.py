# coding:utf-8
import sys
import tools

reload(sys)
sys.setdefaultencoding("utf8")

PV190_ROOTURL = "http://bbs.my8600.com"

OUT_DIR = "D:\\book\\pv190\\"
PV190_FILE = "_20190331_img.txt"
PV190_TORRENT = "_20190331_torrent.txt"
FLAG_FILE = "_20190331_flag.txt"
FLAG = "\0"
HTTP_SPLIT = "http://"


def get_pagecon(ori_param_json):
    print ori_param_json["url"] + "============================"

    flag = ori_param_json["file"]
    torrent_data = ""
    img_data = "\n" + ori_param_json["src"]
    flag_data = "\n%s%s%s" % (flag, FLAG, ori_param_json["src"])
    data_filepath = "%s%s%s" % (OUT_DIR, ori_param_json["dir"].decode('utf8').encode('gb2312'), PV190_FILE)
    torrent_filepath = "%s%s%s" % (OUT_DIR, ori_param_json["dir"].decode('utf8').encode('gb2312'), PV190_TORRENT)
    flag_filepath = "%s%s%s" % (OUT_DIR, ori_param_json["dir"].decode('utf8').encode('gb2312'), FLAG_FILE)

    pagecon = tools.get_html_content(ori_param_json["url"], "div", "class", "pagecon")
    if len(pagecon) <= 0:
        return
    list_ul = pagecon[0].find_all("img")
    for item in list_ul:
        img = item.get("src")
        img_url = "%s%s" % (PV190_ROOTURL, img) if (img.startswith("/")) else img
        print img_url
        img_data = "%s\n%s" % (img_data, img_url)
        flag_data = "%s\n%s%s%s" % (flag_data, flag, FLAG, img_url)

    torrent = pagecon[0].get_text()
    torrent_url_list = torrent.split(HTTP_SPLIT)
    if len(torrent_url_list) <= 1:
        return
    for item in torrent_url_list:
        if item.find(".torrent") >= 0:
            torrent_url = HTTP_SPLIT + item[:(item.find(".torrent") + 8)]
            print torrent_url
            torrent_data = "%s\n%s" % (torrent_data, torrent_url)
            flag_data = "%s\n%s%s%s" % (flag_data, flag, FLAG, torrent_url)

    tools.write_file(torrent_data, torrent_filepath)
    tools.write_file(img_data, data_filepath)
    tools.write_file(flag_data, flag_filepath)


def get_mnewest(ori_param_json):
    print ori_param_json["url"] + "============================"
    mnewest = tools.get_html_content(ori_param_json["url"], "div", "class", "mnewest")
    list_ul = mnewest[0].find_all("a")
    for item in list_ul:
        if len(item.contents) == 2 and item.img:
            # print item
            # print "------------------------------------------------------------"
            # print item.get("href")
            # print item.img.get("src")  # item.img.get("src") AttributeError: 'NoneType' object has no attribute 'get'
            # print item.img.get("title")
            param_json = {}
            param_json["url"] = "%s%s" % (PV190_ROOTURL, item.get("href"))
            img = item.img.get("src")
            param_json["src"] = "%s%s" % (PV190_ROOTURL, img) if(img.startswith("/")) else img
            param_json["dir"] = ori_param_json["dir"]
            param_json["file"] = item.img.get("title")
            get_pagecon(param_json)

    list_ul = mnewest[0].div.find_all("a")
    for item in list_ul:
        if item.get_text().find("下一页") > 0 :
            nextpage_url = item.get("href")
            if len(nextpage_url) > 5:
                param_json = {}
                param_json["url"] = "%s%s" % (PV190_ROOTURL, nextpage_url) if (nextpage_url.startswith("/")) else nextpage_url
                param_json["dir"] = ori_param_json["dir"]
                get_mnewest(param_json)


def get_wp_n_m(ori_url):
    wp_n_m = tools.get_html_content(ori_url, "span", "class", "wp_n_m_r_t")
    # list_ul = wp_n_m[0].ul.contents
    for item in wp_n_m:
        sub_url = item.a.get("href")
        if sub_url.startswith("/"):
            print(item.a.get_text())
            param_json = {}
            param_json["url"] = "%s%s" % (PV190_ROOTURL, sub_url)
            param_json["dir"] = item.a.get_text()
            get_mnewest(param_json)


if __name__ == '__main__':
    print "====================================begin============================================== "
    # get_wp_n_m(PV190_ROOTURL)


    #测试
    param_json = {}
    param_json["url"] = "http://www.pv190.com/a/avwm/index.html"
    param_json["dir"] = "无码"
    get_mnewest(param_json)

    # param_json = {}
    # param_json["url"] = "http://bbs.my8600.com/a/rm/3742.html"
    # param_json["src"] = "11111"
    # param_json["dir"] = "2222"
    # param_json["file"] = "33333"
    # get_pagecon(param_json)

    print "====================================finish============================================== "
