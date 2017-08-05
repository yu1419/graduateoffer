from werkzeug.security import generate_password_hash, check_password_hash
from threading import Thread
from flask import current_app
from .model import Offer, Applicant
from sqlalchemy.sql.expression import and_, distinct
from math import ceil
from sqlalchemy import desc, asc

"""
def get_user(email):
    # get user by email
    user = None
    sql = "select count(*) from user where email = %s"
    count = 0
    with db.cursor() as cursor:
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        if result:
            count = result.get("count(*)", 0)
    db.close()
    if count:
        user = User(email)
    return user


def send_async_email(app, mail, msg):
    with app.app_context():
        mail.send(msg)


def send_email(mail, msg):
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, mail, msg])
    thr.start()
    return thr
"""

def get_sum_offer(db):
    return db.session.query(Offer).\
         filter(Offer.univ_rank != None).count()


def get_sum_applicant(db):
    return db.session.query(Applicant).\
         filter((Applicant.applicant_id == Offer.applicant_id) &
         (Offer.univ_rank != None)).distinct().count()


def get_applicant(db, applicant_id):
    return db.session.query(Applicant).\
         filter(Applicant.applicant_id == applicant_id).first()


def get_app_offer_count(db, person_id):
    result = db.session.query(distinct(Offer.univ_rank)).\
        filter(and_(Offer.person_id ==
               person_id, Offer.univ_rank != None)).count()

    return result


def get_app_offer_count_from_dict(db, data):
    for item in data:

        item["RESULTS"] = get_app_offer_count(db, (item["USER ID"]))


def form_table_data(db, result):
    data = []
    for x in result:
        data.append(x._asdict())
    get_app_offer_count_from_dict(db, data)
    return data


def get_all_univ_name(db):
    result = db.session.query(Offer.univ_rank.label("univ_rank"),
                              Offer.univ_name.label("univ_name")).\
                              filter(Offer.univ_rank != None).\
                              order_by(asc("univ_rank")).distinct().all()
    return result


def convert_string_to_bool(filter_type):
    if (type(filter_type)) == type(""):
        if filter_type == "False":
            filter_type = False
        else:
            filter_type = True
    return filter_type


class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num




"""
def send_email(mail, msg):
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, mail, msg])
    thr.start()
    return thr


def register_user(email, password):
    db = get_db()
    hashed_password = generate_password_hash(password)
    sql = "insert into user (user_name, email, hashed_password) \
           values (%s, %s, %s)"
    with db.cursor() as cursor:
        cursor.execute(sql, (email, email, hashed_password))
        db.commit()
    db.close()


def email_exist(email):
    db = get_db()
    # check if an email has been regisreted or not
    sql = "select count(*) from user where email = %s"
    count = 0
    with db.cursor() as cursor:
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        if result:
            count = result.get("count(*)", "")
    db.close()
    if count:
        return True
    else:
        return False


def valid_login(email, password):
    db = get_db()
    sql = "select hashed_password from user where email = %s"
    hashed_password = ""
    with db.cursor() as cursor:
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        if result:
            hashed_password = result.get("hashed_password", "")
    db.close()
    if check_password_hash(hashed_password, password):
        return True
    else:
        return False


def convert_id(id):
    db = get_db()
    # covert user_id to user email
    sql = "select email from user where user_id = %s"
    email = ""
    with db.cursor() as cursor:
        cursor.execute(sql, id)
        result = cursor.fetchone()
        if result:
            email = result["email"]
    db.close()
    return email


def id_to_username(user_id):
    db = get_db()
    # convert user_id to user name
    sql = "select user_name from user where user_id = %s"
    user_name = None
    with db.cursor() as cursor:
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()
        if result:
            user_name = result["user_name"]
    db.close()
    return user_name


def name_to_id(user_name):
    db = get_db()
    # convert user name to user id
    if not user_name:
        return None
    print("username")
    print(user_name)
    sql = "select user_id from user where user_name = %s"
    user_id = None
    with db.cursor() as cursor:
        cursor.execute(sql, user_name)
        result = cursor.fetchone()
        print("func")
        print(result)
        if result:
            user_id = result["user_id"]
    db.close()
    return user_id


def user_basic(user_id):
    db = get_db()
    # get basic user info by user id
    sql = "select * from user where user_id = %s"
    result = None
    with db.cursor() as cursor:
        cursor.execute(sql, user_id)
        result = cursor.fetchone()
    db.close()
    return result
"""
