from numpy import array
import numpy as np
import io
import base64
import urllib.parse as parse
import string
import random
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def get_total(cursor=None, result=None, degree=None, start=None, stop=None,
              under_cater=None, major=None, count_per_page=None,
              rank_list=None):

        result = clean_striction(result)
        degree = clean_striction(degree)
        under_cater = clean_striction(under_cater)
        major = clean_striction(major)
        if rank_list:
            rank_list = rank_list.split(",")
        striction = """"""
        if result:
            striction = striction + """ and """ + """offer.result='%s' """ \
                % (str(result))
        if degree:
            striction = striction + """ and """ + """offer.degree ='%s' """ \
                % (str(degree))
        if under_cater:
            striction = striction + """ and """ +\
                        """person.under_school_type ='%s' """ % (str(under_cater))
        if rank_list:
            striction = striction + """ and ("""
            for i in range(len(rank_list)):
                if i == 0:
                    striction = striction + """ offer.ranking=%s """%(rank_list[i])
                else:
                    striction = striction + """or offer.ranking=%s """%(rank_list[i])
            striction = striction + """ ) """
        else:
            striction = striction + """ and """ + \
                """offer.ranking>=%s and offer.ranking<=%s """\
                % (str(start), str(stop))
        if major:
            striction = striction + """ and """ + \
                """offer.major_cate='%s' """ % (str(major))


        sql = """select count(*) from offer, person where offer.url = person.url %s""" %(striction)
        cursor.execute(sql)
        total_result = cursor.fetchall()[0][0]

        return total_result



def get_pic(cursor=None, result=None, degree=None, start=None, stop=None,
            under_cater=None, major=None, count_per_page=None, rank_list=None):
    pic_data = None

    result = clean_striction(result)
    degree = clean_striction(degree)
    under_cater = clean_striction(under_cater)
    major = clean_striction(major)
    if rank_list:
        rank_list = rank_list.split(",")

    striction = """"""
    if result:
        striction = striction + """ and """ + """offer.result='%s' """ \
            % (str(result))
    if degree:
        striction = striction + """ and """ + """offer.degree ='%s' """ \
            % (str(degree))
    if under_cater:
        striction = striction + """ and """ +\
                    """person.under_school_type ='%s' """ % (str(under_cater))
    if rank_list:
        striction = striction + """ and ("""
        for i in range(len(rank_list)):
            if i == 0:
                striction = striction + """ offer.ranking=%s """%(rank_list[i])
            else:
                striction = striction + """or offer.ranking=%s """%(rank_list[i])
        striction = striction + """ ) """
    else:
        striction = striction + """ and """ + \
            """offer.ranking>=%s and offer.ranking<=%s """\
            % (str(start), str(stop))
    if major:
        striction = striction + """ and """ + \
            """offer.major_cate='%s' """ % (str(major))

    sql = """select result, ranking, clean_university,major_cate,degree,under_school_type,gpa,toefl, gre,gre_aw, received_date, person.url from offer, person where offer.url = person.url %s """ %(striction)
    cursor.execute(sql)
    results = cursor.fetchall()
    gpa = array([])
    hund_gpa = array([])
    toefl = array([])
    iELTS = array([])
    gre = array([])
    aw = array([])

    for item in results:
        if item[6]:
            if float(item[6]) < 4:
                gpa = np.append(gpa, [float(item[6])])
            elif float(item[6]) > 70:
                hund_gpa = np.append(hund_gpa, [float(item[6])])
        if item[7]:
            if int(item[7]) > 70 and int(item[7]) < 121:
                toefl = np.append(toefl, [int(item[7])])
            elif int(item[7]) < 10:
                iELTS = np.append(iELTS, [float(item[7])])
        if item[8]:
            gre = np.append(gre, [int(item[8])])
        if item[9]:
            aw = np.append(aw, [float(item[9])])

    plt.figure(figsize=(6, 6))
    G = gridspec.GridSpec(3, 2)

    axes_1 = plt.subplot(G[0, 0])
    axes_1.hist(gpa, 15, alpha=0.5)
    gpa_media = np.median(gpa)
    axes_1.text(0.22, 0.9, 'median='+str(gpa_media), ha='center', va='center',
                transform=axes_1.transAxes)
    axes_1.set_title("4.0 Scale GPA distribution")

    axes_2 = plt.subplot(G[0, 1])
    axes_2.hist(hund_gpa, 15, alpha=0.5)
    hund_gpa_median = np.median(hund_gpa)
    axes_2.text(0.22, 0.9, 'median='+str(hund_gpa_median),
                ha='center', va='center',
                transform=axes_2.transAxes)
    axes_2.set_title("100 Scale GPA distribution")

    axes_3 = plt.subplot(G[1, 0])
    axes_3.hist(toefl, 15, alpha=0.5)
    toefl_median = np.median(toefl)
    axes_3.text(0.22, 0.9, 'median='+str(toefl_median),
                ha='center', va='center',
                transform=axes_3.transAxes)
    axes_3.set_title("TOEFL distribution")

    axes_4 = plt.subplot(G[1, 1])
    axes_4.hist(iELTS, 8, alpha=0.5)
    ielts_median = np.median(iELTS)
    axes_4.text(0.22, 0.9, 'median='+str(ielts_median),
                ha='center', va='center',
                transform=axes_4.transAxes)
    axes_4.set_title("IELTS distribution")

    axes_5 = plt.subplot(G[2, 0])
    axes_5.hist(gre, 13, alpha=0.5)
    gre_median = np.median(gre)
    axes_5.text(0.22, 0.9, 'median='+str(gre_median), ha='center', va='center',
                transform=axes_5.transAxes)
    axes_5.set_title("GRE distribution")

    aw_bins = np.linspace(2.5, 6, 20)
    axes_6 = plt.subplot(G[2, 1])
    axes_6.hist(aw, aw_bins, alpha=0.5)
    aw_median = np.median(aw)
    axes_6.text(0.22, 0.9, 'median='+str(aw_median), ha='center',
                va='center', transform=axes_6.transAxes)
    axes_6.set_title("GRE writing distribution")
    st = plt.suptitle("Scores distribution of serach result")

    plt.tight_layout()

    st.set_y(0.95)
    plt.subplots_adjust(top=0.85)

    buf = io.BytesIO()
    plt.gcf().savefig(buf, format='png')
    buf.seek(0)
    pic_data = parse.quote(base64.b64encode(buf.read()))
    plt.close()
    return pic_data


def get_tablelist(cursor=None, result=None, degree=None, start=None, stop=None,
                  under_cater=None, major=None, count_per_page=None, sort=None,
                  page_number=None, order="DESC", rank_list=None):
    table_list = []

    result = clean_striction(result)
    degree = clean_striction(degree)
    under_cater = clean_striction(under_cater)
    major = clean_striction(major)
    print("i")
    if rank_list:
        rank_list = rank_list.split(",")
    striction = """"""
    if result:
        striction = striction + """ and """ + \
            """offer.result='%s' """ % (str(result))
    if degree:
        striction = striction + """ and """ +\
            """offer.degree ='%s' """ % (str(degree))
    if under_cater:
        striction = striction + """ and """ + \
            """person.under_school_type='%s' """ % (str(under_cater))
    if rank_list:
        striction = striction + """ and ("""
        for i in range(len(rank_list)):
            if i == 0:
                striction = striction + """ offer.ranking=%s """%(rank_list[i])
            else:
                striction = striction + """or offer.ranking=%s """%(rank_list[i])
        striction = striction + """ ) """
    else:
        striction = striction + """ and """ + \
            """offer.ranking>=%s and offer.ranking<=%s """\
            % (str(start), str(stop))
    if major:
        striction = striction + """ and """ + \
            """offer.major_cate='%s' """ % (str(major))
    start_count = (int(page_number)-1)*int(count_per_page)
    limit = """ limit %d,%d""" % (int(start_count), int(count_per_page))
    print("k")
    if order == "ASC":
        sql = """select result, ranking, clean_university,major_cate,degree,under_school_type,gpa,toefl, gre,gre_aw, received_date, total_count, person.person_id, offer.url from offer, person, offer_count where offer.person_id = person.person_id and offer_count.person_id= person.person_id %s and (person.version, person.person_id) in (select max(version), person_id from person group by person_id) order by ISNULL(%s) , %s asc %s""" %(striction, sort, sort, limit)
    else:
        sql = """select result, ranking, clean_university,major_cate,degree,under_school_type,gpa,toefl, gre,gre_aw, received_date, total_count, person.person_id, offer.url from offer, person, offer_count where offer.person_id = person.person_id and offer_count.person_id= person.person_id %s and (person.version, person.person_id) in (select max(version), person_id from person group by person_id) order by ISNULL(%s) , %s DESC %s""" %(striction, sort, sort, limit)
    print("j")
    print(sql)
    cursor.execute(sql)
    results = cursor.fetchall()
    print("mm")

    for item in results:
        item_list = [str(i) for i in item]
        url = item_list.pop()
        person_id = item_list.pop()
        count = item_list.pop()
        table_list.append((item_list, count, person_id, url))
    print("l")

    return table_list


def id_table_list(cursor, person_id):
    sql = """select result, ranking, clean_university,major_cate,degree,under_school_type,gpa,toefl, gre,gre_aw, received_date,  offer.url from offer, person where offer.person_id = %s and offer.person_id= person.person_id and (person.version, person.person_id) in (select max(version), person_id from person group by person_id) and ranking is not NULL"""
    cursor.execute(sql, (person_id, ))
    results = cursor.fetchall()
    table_list = []

    for item in results:
        item_list = [str(i) for i in item]
        url = item_list.pop()
        table_list.append((item_list, url))

    return table_list


def autolabel(ax, rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                format(int(height), ",d"),
                ha='center', va='bottom')


def get_first_pic(name, count, label, title):
    plt.figure(figsize=(3, 3))
    x_1 = range(len(name))
    rects1 = plt.bar(x_1, count, alpha=0.5)
    plt.xticks(x_1, name)
    plt.ylim([0, max(count)*1.15])
    plt.title(title)
    autolabel(plt, rects1)
    plt.gcf().subplots_adjust(left=0.15)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.gcf().savefig(buf, format='png')
    buf.seek(0)
    datas = parse.quote(base64.b64encode(buf.read()))
    plt.close()
    return datas


def get_major_univ(db, cursor):
    sql = """select distinct major_cate from offer order by major_cate"""
    cursor.execute(sql)
    results = cursor.fetchall()
    major_list = []
    major_list.append(("All", "All"))
    for item in results:
        major_list.append((item[0], item[0]))
    univ_rank_list = []
    sql = """select distinct ranking, clean_university from offer where ranking is not NULL order by ranking """

    cursor.execute(sql)
    results = cursor.fetchall()
    for item in results:
        if item[0]:
            item = list(item)
            item = str(item[0])+"-"+(item[1])
            univ_rank_list.append(item)
    return major_list, univ_rank_list


def clean_striction(text):
    if text == "All":
        return None
    else:
        return text


def update_visitor(db, cursor, ip):
    sql = """ insert into visitor (ip) values(%s) """
    cursor.execute(sql, (ip, ))
    db.commit()


def get_total_offer(db, cursor):
    sql = """select count(*) from offer where ranking <100"""
    cursor.execute(sql)
    total_offer = cursor.fetchall()
    total_offer = format(int(total_offer[0][0]), ',d')
    return total_offer


def get_result_count(db, cursor, cater):
    sql = ""
    if cater == "result":
        sql = """select result, count(*) from offer where result <> "Other" \
                 and ranking is not NULL group by result order by \
                 count(*) DESC"""
    else:
        sql = """select degree, count(*) from offer where degree <> "Other" \
                 and ranking is not NULL group by degree order by \
                 count(*) DESC"""
    cursor.execute(sql)
    result = cursor.fetchall()

    name = []
    count = []
    label = []

    for item in result:
        item = list(item)
        name.append(item[0])
        count.append(int(item[1]))
        item[1] = format(item[1], ",d")
        label.append(item)

    return name, count, label


def get_under_count(db, cursor, cater):
    # need to replace under_school_type with cater
    sql = """select under_school_type, count(*) from person where \
             (version, person_id) in (select max(version), person_id \
             from person group by person_id) and under_school_type is \
             not NULL group by under_school_type"""
    cursor.execute(sql)
    under_school = cursor.fetchall()

    name = []
    count = []
    label = []

    for item in under_school:
        item = list(item)
        name.append(item[0])
        count.append(int(item[1]))
        item[1] = format(item[1], ',d')
        label.append(item)
    return name, count, label


def clean_userID(userid):
    return userid[userid.index("_")+1:]


def general_random_password():
    char_list = string.ascii_uppercase + string.digits
    pass_list = [random.choice(char_list) for _ in range(8)]
    password = "".join(pass_list)
    return password
