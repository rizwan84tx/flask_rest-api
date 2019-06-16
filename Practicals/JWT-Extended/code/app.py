from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

#from security import authenticate, identity
from resources.user import UserRegister, UserLogin, TokenRefresh
from resources.item import Item, ItemList
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #flask_SQLAlchemy tracks all changes takes more resources, we turn it OFF as SQLAlchemy has its own library that does tracking
app.secret_key = 'rizwan' #key to excrypt the data
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claim_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['identity'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message':'Token has expired',
        'errorCode':'101'
    }),401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify ({
        'message':'Authentication failed',
        'error':'Invalid JWT'
    }), 401

@jwt.unauthorized_loader
def unauthorized_loader_callback():
    return jsonify ({
        'message':'No access token provided'
        'error':'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify ({
        'message':'The token is not fresh'
        'error':'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify ({
        'message':'The token has been revoked'
        'error':'token_revoked'
    }), 401

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=2605, debug=True)
