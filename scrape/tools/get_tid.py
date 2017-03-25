import re


def get_tid(url):
    url = url.strip()
    index = url.find("tid")
    tid = (re.findall("\d+", url[index:]))[0]
    return tid
