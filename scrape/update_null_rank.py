from get_db import get_db
from tools.university import get_uni_rank
from tools.school_rank import get_school_rank
import codecs

university_dict = get_uni_rank()

db, cursor = get_db()
sql = """select university, id from offer where ranking is NULL"""
cursor.execute(sql)
result = cursor.fetchall()
for item in result:
    clean_u, ranking = get_school_rank(university_dict, item[0])
    if ranking:
        sql = """update offer set clean_university= %s, ranking = %s where id =%s"""
        cursor.execute(sql, (clean_u, ranking, item[1]))
        db.commit()
        print("update")
