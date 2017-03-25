from gter_url import Gter_scraper
from point_url import Point_scraper
from get_db import get_db
from tools.get_tid import get_tid
N = 300


def check_exit(cursor, url=None, tid=None):
    has = False
    if tid:
        sql = """select count(*) from all_url where tid = (%s)"""
        cursor.execute(sql, (tid,))
        has = cursor.fetchall()[0][0]
    else:
        sql = """select count(*) from all_url where url = (%s)"""
        cursor.execute(sql, (url, ))
        has = cursor.fetchall()[0][0]
    return has


def add_url(db, cursor, url, tid=None):
    if tid:
        sql = """insert into all_url (url,tid) VALUES (%s, %s)"""
        try:
            cursor.execute(sql, (url, tid))
        except Exception as e:
            print(e)
    else:
        sql = """insert into all_url (url) VALUES (%s)"""
        try:
            cursor.execute(sql, (url, ))
        except Exception as e:
            print(e)
    db.commit()


def update_point():
    point = Point_scraper()
    db, cursor = get_db()
    page = 1
    old_url = 0
    while old_url < N:
        try:
            url_list = point.scrape_page(page)
            for url in url_list:
                if check_exit(cursor, url=url):
                    old_url = old_url + 1
                else:
                    old_url = 0
                    add_url(db, cursor, url)
        except Exception as e:
            print(e)
        page = page + 1
    db.close()


def update_gter():
    point = Gter_scraper()
    db, cursor = get_db()
    page = 1
    old_url = 0
    while old_url < N:
        try:
            url_list = point.scrape_one_page(page)
            for url in url_list:
                tid = get_tid(url)
                if check_exit(cursor, tid=tid):
                    old_url = old_url + 1
                else:
                    old_url = 0
                    add_url(db, cursor, url, tid=tid)
        except Exception as e:
            print(e)
        page = page + 1
    db.close()


def update_all():
    update_point()
    update_gter()

if __name__ == "__main__":
    update_all()
