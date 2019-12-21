import sqlite3
from sqlalchemy_db import db


class UserModel(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def __init__(self, username, password, admin=False):
        self.username = username
        self.password = password
        self.admin = admin


    def toDict(self):
        return {
            "id": self.id,
            "username": self.username,
            "admin": self.admin
        }


    @classmethod
    def find_by_username(cls, username):
        try:
            result = UserModel.query.filter_by(username=username).first()
            return result
        except Exception as e:
            raise Exception(e)


    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.find_by_username(self.username)
        except Exception as e:
            raise Exception(e)


    @classmethod
    def get_all_users(cls):
        try:
            connection = sqlite3.connect("data.database")
            cursor = connection.cursor()
            select_query = "SELECT * FROM users"
            result = cursor.execute(select_query).fetchall()
            connection.close()
            return result
        except Exception as e:
            raise Exception(e)

