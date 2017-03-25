from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


class Point_scraper:
    def __init__(self):
        self.page_number = 1
        self.max_page = 1
        self.thread_pattern = re.compile("normalthread_.*?")
        self.class_name = "s xst"
        self.url_head = "http://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=82&sortid=164&%1=&sortid=164&page="

    def scrape_page(self, page):
        url = self.url_head + str(page)
        html = urlopen(url, timeout=60)
        bsObj = BeautifulSoup(html.read(), "html5lib")
        if bsObj:
            pattern = self.thread_pattern
            all_content = bsObj.findAll("tbody", {"id": pattern})
            class_name = self.class_name
            url_list = []
            for content in all_content:
                try:

                    url = content.find("a", {"class": class_name})["href"]
                    if url:
                        url = url.strip()
                        url_list.append(url)
                except AttributeError as e:
                    print(e)
            return url_list
