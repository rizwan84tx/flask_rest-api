import sqlite3
from flask_restful import Resource, reqparse

class User:
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

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = "user cannot be blank"
        )
    parser.add_argument('password',
        type = str,
        required = True,
        help = "password cannot be blank"
        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']): # Validates the user existance - method 'find_by_username' return None when no user found
            return {"message":"User aleady exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password'],))

        connection.commit()
        connection.close()

        return {"message":"User created successfully"}, 201
