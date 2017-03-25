from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from multiprocessing import Process, Lock, Queue
import time


class Gter_scraper:
    def __init__(self):
        self.page_number = 1
        self.max_page = 1
        self.max_page_class = "last"
        self.link_pattern = re.compile("normalthread_.*?")
        self.link_class = "xst"
        self.url_head = "http://bbs.gter.net/forum.php?mod=forumdisplay&fid=49&typeid=158&filter=typeid&typeid=158&page="

    def scrape_one_page(self, page):
        url = self.url_head + str(page)
        html = urlopen(url, timeout=60)
        bsObj = BeautifulSoup(html.read(), "html5lib")
        all_url = []
        all_content = bsObj.findAll("tbody", {"id": self.link_pattern})
        for content in all_content:
            try:
                url_content = content.find("a", {"class": self.link_class})
                if hasattr(url_content, "href"):
                    all_url.append(url_content["href"])
            except AttributeError as e:
                print(e)
        return all_url

    def get_total_page(self):
        page = 1
        url = self.url_head + str(page)
        html = urlopen(url, timeout = 60)
        bsObj = BeautifulSoup(html.read(), "html5lib")
        content = bsObj.find("a", {"class": self.max_page_class}).getText()
        max_page = re.findall("(\d+)", content)[0]
        if max_page:
            self.max_page = int(max_page)
        else:
            self.max_page = 1


def scrape_all_page(gter, fname, l, page_q):
    while not page_q.empty():
        page_num = page_q.get()
        print("Please wait, processing page " + str(page_num))
        url_list = gter.scrape_one_page(page_num)
        if url_list:
            l.acquire()
            with open(fname, 'a') as f:
                    for row in url_list:
                        f.write(row+"\n")
            l.release()


def save_url(fname):
    a = Gter_scraper()
    a.get_total_page()
    page_q = Queue()
    print("max " + str(a.max_page))
    for page in range(1, a.max_page+1):
        page_q.put(page)
    l = Lock()
    processes = []
    for i in range(50):
        processes.append(Process(target=scrape_all_page,
                                 args=(a, fname, l, page_q)))
    for p in processes:
        p.start()
    for p in processes:
        p.join()
