from bs4 import BeautifulSoup
import re
from tools.clean_data import clean_string, clean_school, clean_result
from tools.clean_data import clean_degree, college_category, major_category
from tools.university import get_school_rank


class Gter_offer:
    def __init__(self, html_content, url):
        self.url = url
        self.offer_pattern = re.compile("offer.*?")
        self.personal_pattern = "个人情况"
        self.id_pattern = re.compile("http://bbs.gter.net/space-uid.*?")
        self.html_content = html_content
        self.bsObj = BeautifulSoup(html_content, "html5lib")
        self.sentece = ""
        self.source = "gter"
        self.get_sentence()

    def get_sentence(self):
        id_pattern = re.compile("postmessage")
        all_sentences = self.bsObj.find("td", {"class": "t_f",
                                               "id": id_pattern})
        sentence_list = all_sentences.findAll(text=True, recursive=False)
        self.sentence = "".join(sentence_list)
        self.sentence = clean_string(self.sentence)

    def current_url(self):
        return self._url

    def get_id(self):
        person_id = self.bsObj.findAll("a", {"href": self.id_pattern})[0]
        if person_id:
            result = person_id.getText()
            if len(result) > 1:
                return result
            else:
                return "Anonymous"
        else:
            return "Anonymous"

    def get_offer_list(self):
        return self.bsObj.findAll("table", {"summary": self.offer_pattern})

    def get_personal_info(self):
        return self.bsObj.findAll("table", {"summary": self.personal_pattern})

    def get_offer_info(self):
        offer_list = self.get_offer_list()
        offer_result = []
        university = None
        degree = None
        major = None
        result = None
        noti_date = None
        clean_univ = None
        ranking = None
        person_id = self.get_id()
        for offer in offer_list:
            info_list = offer.findAll("tr")
            if len(info_list) == 7:
                university_content = info_list[0].td
                if university_content.a:
                    university = clean_school(university_content.a.getText())
                else:
                    university = clean_school(university_content.getText())
                if university:
                    clean_univ, ranking = get_school_rank(university)

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
                offer_result.append((university, degree, major, major_cate,
                                    result, noti_date, clean_univ, ranking,
                                    person_id, self.source, self.sentence,
                                    self.url, self.source))
        return offer_result

    def get_person_detail(self):
        post_content = self.get_personal_info()[0]
        toefl = None
        gre = None
        gre_aw = None
        under_grad = None
        college_type = None
        major = None
        gpa = None
        comment = None

        person_id = self.get_id()

        info_list = post_content.findAll("tr")
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
                college_type = college_category(under_grad)
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

        return toefl, gre, gre_aw, under_grad, college_type,\
            gpa, comment, person_id, self.source


if __name__ == "__main__":
    url = ("http://bbs.gter.net/forum.php?"
           "mod=viewthread&tid=2096538&extra=page%3D1%26filter%3Dauthor%26o"
           "rderby%3Ddateline%26typeid%3D158%26typeid%3D158%26orderby%3D"
           "dateline")

    from get_url import s
    html = s.get(url, timeout=60).content
    gter = Gter_offer(html)
    print(gter.get_offer_info())
