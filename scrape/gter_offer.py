from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time
from tools.clean_data import clean_string, clean_school, clean_result
from tools.clean_data import clean_degree, under_cate, major_category, is_grad
from multiprocessing import Process, Lock, Queue
import codecs
from tools.university import get_uni_rank
from tools.school_rank import get_school_rank
university_dict = get_uni_rank()


class Gter_offer:
    def __init__(self, url):
        self.offer_pattern = re.compile("offer.*?")
        self.personal_pattern = "个人情况"
        self.id_pattern = re.compile("http://bbs.gter.net/space-uid.*?")
        self._url = url
        html = urlopen(self._url, timeout=60)
        self.bsObj = BeautifulSoup(html.read(), "html5lib")

    def current_url(self):
        return self._url

    def get_id(self):
        person_id = self.bsObj.findAll("a", {"href": self.id_pattern})[0]
        return "gter_" + person_id.getText()

    def get_offer_list(self):
        return self.bsObj.findAll("table", {"summary": self.offer_pattern})

    def get_personal_info(self):
        return self.bsObj.findAll("table", {"summary": self.personal_pattern})

    def get_offer_info(self, offer_obj):
        university = None
        degree = None
        major = None
        result = None
        noti_date = None
        clean_univ = None
        ranking = None
        person_id = self.get_id()
        info_list = offer_obj.findAll("tr")
        if len(info_list) == 7:
            university_content = info_list[0].td
            if university_content.a:
                university = clean_school(university_content.a.getText())
            else:
                university = clean_school(university_content.getText())
            if university:
                clean_univ, ranking = get_school_rank(university_dict,
                                                      university)

            degree = clean_degree(info_list[1].td.getText())
            major_content = info_list[2].td
            if major_content.a:
                major = clean_string(major_content.a.getText())
            else:
                major = clean_string(major_content.getText())
            result = clean_result(info_list[3].td.getText())
            noti_date = clean_string(info_list[6].td.getText())
            noti_date = re.findall("\d\d\d\d\-\d+\-\d+", noti_date)
            if noti_date:
                noti_date = noti_date[0]
            else:
                noti_date = None
            major_cate = major_category(major)
            return university, degree, major, major_cate, result, \
                noti_date, clean_univ, ranking, person_id
        else:
            return None

    def get_personal(self, offer_obj):
        toefl = None
        gre = None
        gre_aw = None
        under_grad = None
        under_category = None
        major = None
        gpa = None
        comment = None
        grad = None
        grad_cate = None
        person_id = self.get_id()

        info_list = offer_obj.findAll("tr")
        for item in info_list:
            if "IELTS" in str(item) or "TOEFL" in str(item):
                toefl_list = item.td.getText()
                toefl_number = re.findall("\d+", toefl_list)
                if toefl_number:
                    toefl = int(toefl_number[0])
                    if toefl > 120:
                        toefl = None
            if "GRE" in str(item):
                gre_list = item.td.getText()
                gre_list = re.findall("\d+\.*\d*", gre_list)
                if gre_list:
                    if int(gre_list[0]) > 300:
                        gre = int(gre_list[0])
                        if gre > 340:
                            gre = None
                    if float(gre_list[len(gre_list)-1]) < 7:
                        gre_aw = float(gre_list[len(gre_list)-1])
            if "本科学校" in str(item):
                under_grad = clean_string(item.td.getText())
            if "研究生" in str(item):
                grad = clean_string(item.td.getText())
            if "本科专业" in str(item):
                major = clean_string(item.td.getText())
            if "本科成绩" in str(item):
                gpa_list = item.td.getText()
                gpa_list = re.findall("\d+\.*\d*", gpa_list)
                if gpa_list:
                    gpa = float(gpa_list[0])
                    if not (gpa < 5 or 60 < gpa < 101):
                        gpa = None
            if "其他" in str(item):
                comment = item.td
                if comment:
                    comment = clean_string(comment.getText())
            under_category = under_cate(under_grad)
            grad_cate = is_grad(grad)

        return toefl, gre, gre_aw, under_grad, under_category, grad,\
            grad_cate, major, gpa, comment, person_id


def save_result(urlqueue, fpname, foname, erro_file, l_offer, l_person, l_erro):
    while not urlqueue.empty():
        url_list = urlqueue.get()
        for url in url_list:
            try:
                url = url.replace("\n", "")
                a = Offer_page(url)
                info = a.get_personal_info()[0]
                toefl, gre, gre_aw, under_grad, under_category, grad, grad_cate, \
                    major, gpa, comment = a.get_personal(info)
                try:
                    l_person.acquire()
                    with codecs.open(fpname, "a", "utf-8") as f:
                        f.write((str(toefl)) + "\t" + (str(gre)) + "\t" +
                                (str(gre_aw)) + "\t" + (str(under_grad)) + "\t" +
                                (str(under_category)) + "\t" + (str(grad)) + "\t" +
                                (str(grad_cate)) + "\t" + (str(major)) + "\t" +
                                str(gpa) + "\t" + (str(comment)) + "\t" + str(url))
                finally:
                    l_person.release()
                offer_list = a.get_offer_list()
                for offer in offer_list:
                    university, degree, major, major_cate, result,\
                        noti_date, clean_univ, ranking = a.get_offer_info(offer)
                    try:
                        l_offer.acquire()
                        with codecs.open(foname, "a", "utf-8") as f:
                            f.write((str(university)) + "\t" + (str(degree)) +
                                    "\t" + (str(major)) + "\t" +
                                    (str(major_cate)) + "\t" + (str(result)) +
                                    "\t" + (str(noti_date)) + "\t" + str(url) +
                                    "\t" + str(clean_univ) + "\t" + str(ranking) +
                                    "\n")
                    finally:
                        l_offer.release()
            except Exception as e:
                with open(erro_file, "a") as f:
                    f.write(url+"  <---")
                    f.write(str(e)+"\n")

if __name__ == "__main__":
    url = "http://bbs.gter.net/forum.php?mod=viewthread&tid=2074159&extra=page%3D1%26filter%3Dtypeid%26typeid%3D158%26typeid%3D158"
    gter = Gter_offer(url)
    info = gter.get_personal_info()[0]
    c = gter.get_offer_list()[0]
    print(gter.get_offer_info(c))
