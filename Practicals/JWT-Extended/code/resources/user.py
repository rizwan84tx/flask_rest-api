import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_refresh_token_required,get_jwt_identity

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

class UserLogin(Resource):
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
        #get data from parser
        data = self.parser.parse_args()

        #find user in database
        user = UserModel.find_by_username(data['username'])

        #check password
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True) #create access token
            refresh_token = create_refresh_token(user.id) #create refresh token
            return{
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, 200
        #return token
        return {'message': 'Invalid Credentials'}, 401

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False) #create non-fresh token
        return {'access_token': new_token}, 200
