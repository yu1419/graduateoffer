from bs4 import BeautifulSoup
import re
from tools.clean_data import clean_string, clean_degree, clean_result
from tools.clean_data import college_category, major_category
from tools.university import get_school_rank


class Point_offer:
    def __init__(self, html_content, url):
        self.html_content = html_content
        self.url=url
        self.bsObj = None
        self.first_post = None
        self.title = None
        self.sentence = ""
        self.source = "point"
        self.get_first_post()
        self.get_title()
        self.get_info_list()
        self.get_sentence()
        self.id_pattern = re.compile("http://www.1point3acres.com"
                                     "/bbs/space-uid.*?")

    def get_id(self):
        person_id = self.first_post.findAll("a", {"href": self.id_pattern})[0]
        return person_id.getText()

    def get_sentence(self):
        id_pattern = re.compile("postmessage")
        all_sentences = self.first_post.findAll("td", {"class": "t_f",
                                                "id": id_pattern})[0]
        sentence_list = all_sentences.findAll(text=True, recursive=False)
        self.sentence = "".join(sentence_list)
        self.sentence = clean_string(self.sentence)

    def get_first_post(self):
        pattern = re.compile("post_.*?")
        self.bsObj = BeautifulSoup(self.html_content, "html5lib")
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
        degree = clean_degree(self.title)
        major, university = get_university(self.title)
        for maj in major:
            cate = major_category(maj)
            major_cate.append(cate)
        result = clean_result(self.title)
        offer_time = get_time(self.title)
        if university:
            for u in university:
                clean_u, ranking = get_school_rank(u)
                clean_univ.append(clean_u)
                rank_list.append(ranking)
        return major, major_cate, degree, university, result, \
            offer_time, clean_univ, rank_list, person_id, \
            self.sentence, self.url, self.source

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
        under_cate = "other"
        comment = None
        person_id = self.get_id()
        for item in self.info_list:
            text = item.getText()
            if "本科" in text:
                gpa = get_gpa(text)
                under_cate = college_category(text)
            if "T单项" in text:
                toefl = get_Tofel(text)
            if "G单项" in text:
                gre, aw = get_GRE(text)
            if "其他说明" in text:
                comment = get_app_background(text)
                comment = clean_string(comment)
        return gpa, toefl, gre, aw, under_cate, comment, person_id, self.source


def get_gpa(text):
    gpa = None
    gpa_list = re.findall("\d+\.*\d*", text)
    if gpa_list:
        gpa = float(gpa_list[0])
        if not (gpa < 5 or 60 < gpa < 101):
            gpa = None
    return gpa


def get_Tofel(text):
    # do not store IELTS
    content = text.split(":")
    tofel = content[1:]
    string_result = []
    int_result = []
    for score in tofel:
        string_result.extend(re.findall('\d+', score))
    if len(string_result) > 0:
        for score in string_result:
            int_result.append(int(score))
        tofel_score = max(int_result)
        if tofel_score > 60:
            return tofel_score
        else:
            return None
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


def get_time(title):
    time = re.findall("\d\d\d\d\-\d+\-\d+", title)
    if time:
        return time[0]
    else:
        return None


if __name__ == "__main__":
    url = ("http://www.1point3acres.com/bbs/forum.php?"
           "mod=viewthread&tid=286466&extra=page%3D1%26filter"
           "%3Dauthor%26orderby%3Ddateline%26sortid%3D164%26s"
           "ortid%3D164%26orderby%3Ddateline")
    from get_url import s
    html = s.get(url, timeout=60).content
    page = Point_offer(html)
    print(page.sentence)
