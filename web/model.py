from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



model.py


class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

    def update_passowrd(self, old, new):
        pass
