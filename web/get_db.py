
import pymysql


def get_db():
    db = pymysql.connect("offer.cspfrhhjhhea.us-east-1.rds.amazonaws.com",
                         "master", "yusisheng123", "offer_1", charset='utf8')
    cursor = db.cursor()
    return db, cursor
