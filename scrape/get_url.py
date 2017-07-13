from bs4 import BeautifulSoup
import re
import requests
import time

post_pattern = re.compile("normalthread_.*?")
# normal link has a id start with normalthread
# links stick to the top page do not have id start with normalthread

url_class_name = "s xst"  # url exsit in url_class_name <a>

url_head = ("http://www.1point3acres.com/bbs/forum.php?"
            "mod=forumdisplay&fid=82&orderby=dateline"
            "&sortid=164&orderby=dateline&sortid=164"
            "&filter=author&page=")
# url head can find offer links ordered by published date


s = requests.Session()


def scrape_page(page, connect_session, url_head, post_pattern, url_class_name):
    # get offer links for each page

    url = url_head + str(page)
    html = s.get(url, timeout=60).content

    bsObj = BeautifulSoup(html, "html5lib")
    if bsObj:
        pattern = post_pattern
        all_content = bsObj.findAll("tbody", {"id": pattern})
        url_list = []
        for content in all_content:
            try:
                url = content.find("a", {"class": url_class_name})["href"]
                if url:
                    url = url.strip()
                    url_list.append(url)
            except AttributeError as e:
                print(e)
        return url_list


def get_tid(url):
    # get tid from url
    # url example: (http://www.1point3acres.com/bbs/forum.php?
    #  mod=viewthread&tid=286466&extra=page%3D1%26filter%3
    #  Dauthor%26orderby%3Ddateline%26sortid%3D164%26sortid
    #  %3D164%26orderby%3Ddateline)

    tid = re.search("tid=(\d+)", url).group(1)
    return str(tid)

if __name__ == "__main__":
    url_head = ("http://bbs.gter.net/forum.php?"
                "mod=forumdisplay&fid=49&orderby=dateline&"
                "typeid=158&filter=author&orderby=dateline&typeid=158&page=")
    # sorted by posted date

    post_pattern = re.compile("normalthread_.*?")  # nomal post pattern

    url_class_name = "xst"  # url exsit in url_class_name <a>
    start_time = time.time()
    for i in range(1, 10):
        print(scrape_page(i, s, url_head, post_pattern, url_class_name))
    stop_time = time.time()
    print("connection: "+str(stop_time-start_time)+"\n")
