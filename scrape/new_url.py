from get_url import scrape_page, get_tid
import re
from model import Session, All_url
import threading
import logging
N = 100

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s\
                    [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='update_url.log',
                    filemode='a')

#  default variables for scrape 1point3acres website

url_head_1 = ("http://www.1point3acres.com/bbs/forum.php?"
              "mod=forumdisplay&fid=82&orderby=dateline"
              "&sortid=164&orderby=dateline&sortid=164"
              "&filter=author&page=")
# url head can find offer links ordered by published date
post_pattern_1 = re.compile("normalthread_.*?")
# normal link has a id start with normalthread
# links stick to the top page do not have id start with normalthread

url_class_name_1 = "s xst"  # url exsit in url_class_name <a>


# default variables for scrape gter website
url_head_g = ("http://bbs.gter.net/forum.php?"
              "mod=forumdisplay&fid=49&orderby=dateline&"
              "typeid=158&filter=author&orderby=dateline&typeid=158&page=")
# sorted by posted date

post_pattern_g = re.compile("normalthread_.*?")  # nomal post pattern

url_class_name_g = "xst"  # url exsit in url_class_name <a>


def check_exit(s, tid, source):
    result = s.query(All_url).filter(All_url.tid == tid and
                                     All_url.source == source).count()
    return result != 0


def add_url(s, url, source, tid):
    c_url = All_url(url=url, source=source, tid=tid)
    s.add(c_url)
    s.commit()


def update_url(s, url_head, post_pattern, url_class_name, source):
    page = 136
    old_url = 0
    tid = 0
    while old_url < N:
        try:
            url_list = scrape_page(page, s, url_head,
                                   post_pattern, url_class_name)
            logging.info('scrape url in ' + source + ":page-" + str(page))
            for url in url_list:
                tid = get_tid(url)
                if check_exit(s, tid, source):
                    old_url = old_url + 1
                else:
                    old_url = 0
                    add_url(s, url, source, tid)
        except Exception as e:
            print(e)
        page = page + 1


def update_point():
    session_1 = Session()
    update_url(session_1, url_head_1, post_pattern_1,
               url_class_name_1, "point")


def update_gter():
    session_2 = Session()
    update_url(session_2, url_head_g, post_pattern_g, url_class_name_g, "gter")


def update_all():
    #update_gter()
    update_point()



if __name__ == "__main__":
    update_all()
