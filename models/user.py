import sqlite3
from db import db

class UserModel(db.Model):
    # note that UserModel is an api with exposed methods (not a REST api)
    # this defines the database table we are working with
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password=password

    def save_to_db(self): # this replaces both insert and update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first() #select * from users where usernamename=?

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first() #select * from users where id=?
