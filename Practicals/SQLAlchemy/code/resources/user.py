import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

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

        if UserModel.find_by_username(data['username']): # Validates the user existance - method 'find_by_username' return None when no user found
            return {"message":"User aleady exists"}, 400

        user = UserModel(**data) #**data = data['username'], data['password']
        user.save_to_db()

        return {"message":"User created successfully"}, 201
