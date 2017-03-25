from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from multiprocessing import Process, Lock, Queue
from tools.clean_data import clean_string
from tools.clean_data import under_cate, major_category
from tools.university import get_uni_rank
from tools.school_rank import get_school_rank
import codecs

university_dict = get_uni_rank()


class Point_offer:
    def __init__(self, url):
        self._url = url.strip()
        self.bsObj = None
        self.first_post = None
        self.title = None
        self.get_first_post()
        self.get_title()
        self.get_info_list()
        self.id_pattern = re.compile("http://www.1point3acres.com/bbs/space-uid.*?")

    def get_id(self):
        person_id = self.first_post.findAll("a", {"href": self.id_pattern})[0]
        return "point_" + person_id.getText()

    def get_first_post(self):
        pattern = re.compile("post_.*?")
        html = urlopen(self._url, timeout=60)
        self.bsObj = BeautifulSoup(html.read(), "html5lib")
        post_list = self.bsObj.find("div", {"id": "postlist"})
        self.first_post = post_list.find("div", {"id": pattern})

    def get_title(self):
        title = self.first_post.find("u").getText()
        self.title = title

    def get_offer(self):
        university = []
        clean_univ = []
        rank_list = []
        major = []
        major_cate = []
        result = None
        offer_time = None
        degree = None
        person_id = self.get_id()
        degree = get_degree(self.title)
        major, university = get_university(self.title)
        for maj in major:
            cate = major_category(maj)
            major_cate.append(cate)
        result = get_result(self.title)
        offer_time = get_time(self.title)
        if university:
            for u in university:
                clean_u, ranking = get_school_rank(university_dict, u)
                clean_univ.append(clean_u)
                rank_list.append(ranking)
        return major, major_cate, degree, university, result, \
            offer_time, clean_univ, rank_list, person_id

    def get_info_list(self):
        all_list = self.first_post.findAll("li")
        if len(all_list) >= 10:
            self.info_list = all_list[:10]
        else:
            self.info_list = None

    def get_person_info(self):
        toefl = None
        gpa = None
        gre = None
        aw = None
        under_category = "other"
        is_grad_stu = None
        comment = None
        person_id = self.get_id()
        for item in self.info_list:
            text = item.getText()
            if "本科" in text:
                gpa = get_gpa(text)
                under_category = under_cate(text)
            if "T单项" in text:
                toefl = get_Tofel(text)
            if "G单项" in text:
                gre, aw = get_GRE(text)
            if "其他说明" in text:
                comment = get_app_background(text)
                comment = clean_string(comment)
            if "研究生" in text:
                if len(text) > 20:
                    is_grad_stu = True
        return gpa, toefl, gre, aw, under_category, is_grad_stu, comment, person_id


def get_gpa(text):
    gpa = None
    gpa_list = re.findall("\d+\.*\d*", text)
    if gpa_list:
        gpa = float(gpa_list[0])
        if not (gpa < 5 or 60 < gpa < 101):
            gpa = None
    return gpa


def get_Tofel(text):
    content = text.split(":")
    tofel = content[1:]
    string_result = []
    int_result = []
    for score in tofel:
        string_result.extend(re.findall('\d+', score))
    if len(string_result) > 0:
        for score in string_result:
            int_result.append(int(score))
        return max(int_result)
    else:
        return None


def get_GRE(text):
    content = text.split(":")
    gre = content[1:]
    string_result = []
    for score in gre:
        string_result.extend(re.findall("(\d+\.*\d*)", score))
    total, aw = convert_GRE(string_result)
    if total:
        if total > 340 or total < 300:
            total = None
    if aw:
        if aw > 6 or aw < 0:
            aw = None
    return total, aw


def convert_GRE(string_list):
    int_list = []
    for item in string_list:
        int_list.append(float(item))
    total = None
    aw = None
    if len(int_list) == 0:
        return total, aw
    if max(int_list) > 170:
        total = int(max(int_list))
    if min(int_list) < 7:
        aw = min(int_list)
    each_list = []
    if total is None:
        for each in int_list:
            if 130 < each < 171:
                each_list.append(each)
        if len(each_list) != 2:
            return int(total), aw
        else:
            return int(sum(each_list)), aw
    else:
        return total, aw


def get_app_background(text):
    result = text.split(":")
    if len(result) == 1 or result[1:] == ["  "]:
        return None
    else:
        return result[1]


def get_university(title):
    major = []
    university = []
    content_list = re.findall("[a-zA-Z\/]+\@[a-zA-Z\ ]+", title)
    for item in content_list:
        item_list = item.split("@")
        if len(item_list) == 2:
            major.append(item_list[0])
            university.append(item_list[1])
    return major, university


def get_result(title):
    content_list = re.findall("[a-zA-Z]", title)
    content = ("".join(content_list)).lower()
    if "rej" in content:
        return "Rejection"
    elif "offer" in content:
        return "Offer"
    elif "ad" in content:
        return "Ad"
    elif "wl" in content or "wait" in content:
        return "Wait_list"
    else:
        return "Other"


def get_time(title):
    time = re.findall("\d\d\d\d\-\d+\-\d+", title)
    if time:
        return time[0]
    else:
        return None


def get_degree(title):
    title = (clean_string(title)).lower()
    if "ms" in title or "master" in title:
        return "Master"
    elif "phd" in title:
        return "PhD"
    else:
        return None


def test_function(url_q, fperson, foffer, ferror, lp, lo):
    while not url_q.empty():
        url_list = url_q.get()
        for url in url_list:
            try:
                url = url.replace("\n", "")
                a = Offer_page(url)
                major, major_cate, degree, university, result, \
                    offer_time, clean_univ, rank_list = a.get_offer()
                for i in range(len(major)):
                    try:
                        lo.acquire()
                        with codecs.open(foffer, "a", "utf-8") as f:
                            f.write((str(university[i])) + "\t" +
                                    (str(degree)) + "\t" + (str(major[i])) +
                                    "\t" + (str(major_cate[i])) + "\t" +
                                    (str(result)) + "\t" + (str(offer_time)) +
                                    "\t" + str(url) + "\t" +
                                    str(clean_univ[i]) + "\t" +
                                    str(rank_list[i]) + "\t" + str(a.title) +
                                    "\n")
                    finally:
                        lo.release()
                gpa, toefl, gre, aw, under_category, is_grad_stu, comment =\
                    a.get_person_info()
                try:
                    lp.acquire()
                    with codecs.open(fperson, "a", "utf-8") as f:
                        f.write(str(toefl) + "\t" + str(gre) + "\t" + str(aw) +
                                "\t" + str(under_category) + "\t" +
                                str(is_grad_stu) + "\t" + str(gpa) + "\t" +
                                str(comment) + "\t" + str(url))
                finally:
                    lp.release()
            except Exception as e:
                with open(ferror, "a") as f:
                    f.write(url+"  <---")
                    f.write(str(e)+"\n")

if __name__ == "__main__":
    url = "http://www.1point3acres.com/bbs/thread-256557-1-1.html"
    a = Point_offer(url)
    print(a.get_person_info())
