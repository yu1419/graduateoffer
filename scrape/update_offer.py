from point_offer import Point_offer as Point
from gter_offer import Gter_offer as Gter
from multiprocessing import Process, Lock, Queue
from model import Session, All_url, Applicant, Offer, update_version
from time import sleep
import requests
import logging


PROCESS_TIMEOUT = 60*4


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s\
                    [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='update_offer.log',
                    filemode='a')

N_URL_TO_HTML = 4  # process
N_ADD_DATABASE = 14
EAMPTY_HTML_SLEEP_TIME = 5
EAMPTY_HTML_OCCUR_TIMES = 3


def update_point_offer(html_content, url, session, lock):
    try:
        p = Point(html_content, url)
        major, major_cate, degree, university, result, \
            offer_time, clean_univ, rank_list, person_id, \
            sentence, url, source = p.get_offer()
        gpa, toefl, gre, aw, under_cate, comment, person_id, source =\
            p.get_person_info()
        applicant = Applicant(gpa=gpa, toefl=toefl, gre=gre, gre_aw=aw,
                              college_type=under_cate, comment=sentence,
                              person_id=person_id, source=source)
        exist_id = update_version(session, applicant)
        if not exist_id:
            session.add(applicant)
            try:
                lock.acquire()
                session.commit()
                applicant_id = applicant.applicant_id
            except Exception as e:
                logging.debug('erro in offer ' + url + ":" + str(e))
                #
            finally:
                lock.release()
        else:
            applicant_id = exist_id

        for i in range(len(rank_list)):
            offer = Offer(raw_major=major[i], major=major_cate[i],
                          degree=degree, raw_univ_name=university[i],
                          result=result, result_time=offer_time,
                          univ_name=clean_univ[i], univ_rank=rank_list[i],
                          url=url, person_id=person_id, comment=sentence,
                          applicant_id=applicant_id,
                          source=source)
            session.add(offer)
            try:
                lock.acquire()
                session.commit()
            except Exception as e:
                logging.debug('erro in offer ' + url + ":" + str(e))
                #
            finally:
                logging.info('in offer ' + url +
                             ":" + "add offer sucess")
                lock.release()

    except Exception as e:
        logging.debug('erro in offer ' + url + ":" + str(e))
    finally:
        current_url = session.query(All_url).\
            filter(All_url.url == url).first()
        current_url.scraped = True
        try:
            lock.acquire()
            session.commit()
        except Exception as e:
            logging.debug('erro in offer ' + url + ":" + str(e))
        finally:
            lock.release()

        #


def update_gter_offer(html, url, session, lock):
    try:
        applicant_id = None
        g = Gter(html, url)
        toefl, gre, aw, under_grad, college_category,\
            gpa, comment, person_id, source = g.get_person_detail()
        try:
            applicant = Applicant(gpa=gpa, toefl=toefl, gre=gre, gre_aw=aw,
                                  college_type=college_category,
                                  comment=comment,
                                  person_id=person_id, source=source)
            exist_id = update_version(session, applicant)
            if not exist_id:
                session.add(applicant)
                try:
                    lock.acquire()
                    session.commit()
                    applicant_id = applicant.applicant_id
                    if person_id == "Anonymous":
                        applicant.person_id = person_id + str(applicant_id)
                        person_id = applicant.person_id
                except Exception as e:
                    logging.debug('erro in offer ' + url + ":" + str(e))
                finally:
                    lock.release()
            else:
                applicant_id = exist_id
        except Exception as e:
            logging.debug('erro in offer ' + url + ":" + str(e))
            #
        if not applicant_id:
            logging.debug('erro in offer ' + url + ":" + "no app_id")
            offer_list = []
        offer_list = g.get_offer_info()
        for offer_detail in offer_list:
            try:
                (university, degree, major, major_cate,
                 result, noti_date, clean_univ, ranking,
                 person_id, source, sentence,
                 url, source) = offer_detail
                offer = Offer(raw_major=major, major=major_cate,
                              degree=degree, raw_univ_name=university,
                              result=result, result_time=noti_date,
                              univ_name=clean_univ, univ_rank=ranking,
                              url=url, person_id=person_id, comment=sentence,
                              source=source, applicant_id=applicant_id)
                session.add(offer)
                try:
                    lock.acquire()
                    session.commit()
                except Exception as e:
                    logging.debug('erro in offer ' + url + ":" + str(e))
                    #
                finally:
                    lock.release()
                logging.info('in offer ' + url +
                             ":" + "add offer sucess")

            except Exception as e:
                logging.debug('erro in offer ' + url + ":" + str(e))
                #
    except Exception as e:
        logging.debug('erro in offer ' + url + ":" + str(e))

    finally:
        current_url = session.query(All_url).\
            filter(All_url.url == url).first()
        current_url.scraped = True
        try:
            lock.acquire()
            session.commit()
        except Exception as e:
            logging.debug('erro in offer ' + url + ":" + str(e))
        finally:
            lock.release()

        #


def update_one_offer(session, lock, html_q):
    eampty = 0
    while True:
        if not html_q.empty():
            eampty = 0
            html, url, source = html_q.get(timeout=10)
            if source == "gter":
                update_gter_offer(html, url, session, lock)
            else:
                update_point_offer(html, url, session, lock)
        else:
            print("empty:" + str(eampty))
            eampty += 1
            sleep(EAMPTY_HTML_SLEEP_TIME)
            if eampty > EAMPTY_HTML_OCCUR_TIMES:
                break


def get_html(s, html_q, url_q):
    while True:
        if not url_q.empty():
            url, source = url_q.get(timeout=10)
            html = s.get(url, timeout=50).content
            html_q.put((html, url, source))
        else:
            print("all url has been passed to html")
            break


def update_all_offer():
    add_offer = True
    sql_session = Session()
    while add_offer:
        print("new session--------------------")

        sql_session.commit()
        url_list = sql_session.query(All_url).\
            filter(All_url.scraped == False).\
            limit(100)
        if url_list.count() == 0:
            print("no url sleep available")
        else:
            html_q = Queue()
            url_q = Queue()
            l = Lock()
            for url in url_list:
                url_q.put((url.url, url.source))
            task = []
            for i in range(N_URL_TO_HTML):
                s = requests.Session()
                task.append(Process(target=get_html,
                                    args=(s, html_q, url_q)))
            sql_session_list = []
            for i in range(N_ADD_DATABASE):
                sql_session_list.append(Session())

                task.append(Process(target=update_one_offer,
                                    args=(sql_session_list[i], l, html_q)))
            for p in task:
                p.start()

            for p in task:
                p.join(PROCESS_TIMEOUT)
            for i in sql_session_list:
                i.close()

            print("finished 1000 or all")


if __name__ == "__main__":
    update_all_offer()
