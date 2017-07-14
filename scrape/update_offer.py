from point_offer import Point_offer as Point
from gter_offer import Gter_offer as Gter
from get_db import get_db
from multiprocessing import Process, Lock, Queue


N = 1 # process

def update_point_offer(url, cursor, db, lock):
    try:
        a = Point(url)
        major, major_cate, degree, university, result, \
            offer_time, clean_univ, rank_list, person_id = a.get_offer()
        gpa, toefl, gre, aw, under_category, is_grad_stu, comment, person_id =\
            a.get_person_info()
        sql = """insert into person (toefl, gre, gre_aw, under_school_type, is_graduate, gpa, comment, url, person_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            lock.acquire()
            cursor.execute(sql,(toefl, gre, aw, under_category, is_grad_stu, gpa, comment, url, person_id))
            db.commit()
        except Exception as e:
            print(e)
            print(url)
        finally:
            lock.release()

        for i in range(len(rank_list)):

            sql = """insert into offer (major, major_cate, degree, university, result, received_date, clean_university, ranking, url, person_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            try:
                lock.acquire()
                cursor.execute(sql,(major[i], major_cate[i], degree, university[i], result, offer_time, clean_univ[i], rank_list[i], url, person_id))
                db.commit()
            except Exception as e:
                print(e)
                print(url)
            finally:
                lock.release()
    except Exception as e:
        print(e)
        print(url)


def update_gter_offer(url, cursor, db, lock):
    try:
        a = Gter(url)
        info = a.get_personal_info()[0]
        toefl, gre, gre_aw, under_grad, under_category, grad, grad_cate, \
            major, gpa, comment, person_id = a.get_personal(info)
        try:
            sql = """insert into person (toefl, gre, gre_aw, under_school_type, is_graduate, gpa, comment, url, person_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s, %s)"""
            try:
                lock.acquire()
                cursor.execute(sql,(toefl, gre, gre_aw, under_category, grad_cate, gpa, comment, url, person_id))
                print(toefl)
                db.commit()
            except Exception as e:
                print(e)
                print(url)
            finally:
                lock.release()
        except Exception as e:
            print(e)
            print(url)
        offer_list = a.get_offer_list()
        for offer in offer_list:
            try:
                university, degree, major, major_cate, result,\
                    noti_date, clean_univ, ranking, person_id = a.get_offer_info(offer)
                sql = """insert into offer (major, major_cate, degree, university, result, received_date, clean_university, ranking, url, person_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"""
                try:
                    lock.acquire()
                    cursor.execute(sql,(major,major_cate,degree,university,result,noti_date,clean_univ,ranking,url,person_id))
                    print(major)
                    db.commit()
                except Exception as e:
                    print(e)
                    print(url)
                finally:
                    lock.release()

            except Exception as e:
                print(e)
                print(url)
    except Exception as e:
        print(e)
        print(url)


def update_one_offer(q, lock):
    db, cursor = get_db()
    while not q.empty():
        url = q.get()
        if "gter" in url:
            update_gter_offer(url, cursor, db, lock)
        else:
            update_point_offer(url, cursor, db, lock)
        try:
            lock.acquire()
            sql = """update all_url set scraped = 1 where url = %s"""
            cursor.execute(sql, (url, ))
            db.commit()
        finally:
            lock.release()
    db.close()


def update_all_offer():
    add_offer = True
    while add_offer:
        db, cursor = get_db()
        sql = """select all_url.url from all_url where scraped = 0 limit 1000"""
        cursor.execute(sql)
        results = cursor.fetchall()
        url_q = Queue()
        l = Lock()
        if results:
            for item in results:
                url_q.put(item[0])
            task = []
            for i in range(N):
                task.append(Process(target=update_one_offer,
                                         args=(url_q,l,)))
            for p in task:
                p.start()
            for p in task:
                p.join()
        else:
            add_offer = False
        db.close()


if __name__ == "__main__":
    update_all_offer()
