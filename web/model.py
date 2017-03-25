from flask_login import UserMixin
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

    def update_passowrd(self, old, new):
        db = pymysql.connect("offer.cspfrhhjhhea.us-east-1.rds.amazonaws.com", "master", "yusisheng123", "Offer")
        cursor = db.cursor()
        sql = """select password from user where email =%s"""
        cursor.execute(sql, (self.id,))
        hashed_pass = cursor.fetchone()[0]
        valid = check_password_hash(hashed_pass, old)
        if valid:
            new = generate_password_hash(new)
            sql = """update user set password = %s where email = %s"""
            cursor.execute(sql, (new, self.id))
            db.commit()
            db.close()
            return True
        else:
            db.close()
            return False
