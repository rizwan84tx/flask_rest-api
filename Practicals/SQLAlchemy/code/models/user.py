import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor =  connection.cursor()

        query = "SELECT * FROM users WHERE username=?" # Filters the DB with matching username
        result = cursor.execute(query, (username,)) # Get user info that matches; input must be always in tuple format eg(username,)
        row = result.fetchone() #get the 1st matching row

        if row:
            #user = User(row[0], row[1], row[2]) # User is the class, it can be defined via @classmethod using cls
            user = cls(*row) # cls point to User class when calling decorator @classmethod via *xargs
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_userid(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query,(_id,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user
