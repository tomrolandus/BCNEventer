from .__init__ import db
from flask_login import UserMixin


class User(UserMixin, db.Document):

    meta = {'collection': 'users'}
    email = db.StringField()
    password = db.StringField()

    def __repr__(self):
        return 'email: '+self.email+', password: '+self.password

    def __str__(self):
        return 'my str'

