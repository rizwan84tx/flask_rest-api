##### JWT Extended #####
In venv terminal "pin install flask_jwt_extended"

1) In app.py import Extended
from flask_jwt_extended import JWTManager

2) Linking JWTManager with app; however this does not create 'auth' endpoint
jwt =  JWTManager(app)

3) Create 'auth' endpoint in /resources/user.py
class UserLogin

4) Import UserLogin in app.py

5) Create API endpoint for UserLogin
api.add_resource(UserLogin, '/login')

6) In API import flask_jwt_extended (/resources/item.py)
from flask_jwt_extended import jwt_required

7) For API call that requires JWT, define decorator
@jwt_required

------------- CLAIMS ----------------
CLAIMS in flask_jwt_extended are just pieces of data that can be attached to JWT payload
CLAIMS used to add extra data when JWT comes back to us

1) Add a claim under JWTManager in app.py
@jwt.user_claims_loader
def add_claim_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return{'is_admin': False}

2) Using claims in API resources (items.py) import 'get_jwt_claims'
from flask_jwt_extended import jwt_required, get_jwt_claims

@jwt_required
def delete(self, name):
    claims = get_jwt_claims()
    if not claims['is_admin']:
        return {'message': 'You need to an Admin to perform this'}, 401
    item = ItemModel.find_by_name(name)
    if item:
        item.delete_from_db()
    return {"message": "Item deleted"}

------------ JWT OPTIONAL -------------
jwt_optional: Can be added to any endpoint and let you add that jwt can or cannot be present.
Inside the endpount we can choose what to do if jwt is present.
It allows endpoint to return data based on user logged in

1) IMPORT: from flask_jwt_extended import jwt_optional

2) Validate user logged in via 'get_jwt_identity'
from flask_jwt_extended import get_jwt_identity

class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity() # VERIFY THAT USER IS LOGGED IN
        items = [item.json() for item in ItemModel.query.all()]
        if user_id:
            return {'items': items}, 200
        return {'items': "User not logged in"},200
--------------- TOKEN REFRESH -------------------
1) create a new class under resources\user.py

2) Import decorator jwt_refresh_token_required and get_jwt_identity from flask_jwt_extended

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False) #create non-fresh token
        return {'access_token': new_token}, 200

3) In app.py import class TokenRefresh and add api resource and endpoint (/refresh)
from resources.user import UserRegister, UserLogin, TokenRefresh
api.add_resource(TokenRefresh, '/refresh')

4) How to demand fresh token for any endpoint
a) import fresh_jwt_required from flask_jwt_extended
b) declare @fresh_jwt_required for endpoint

@fresh_jwt_required
def post(self, name):
    if ItemModel.find_by_name(name):
        return {'message':"Item {} already exists".format(name)}, 400
    data = Item.parser.parse_args()
    item = ItemModel(name, data['price'])
    try:
        item.save_to_db()
    except:
        return {"message":"An error occured while inserting item"}, 500
    return item.json(), 201
--------------- TOKEN EXPIRED -------------------
@jwt.expired_token_loader
 This decorator is used to when a jwt token has expired and what message needs to be notified for the expired token.

@jwt.expired_token_loader
def expired_token_callback():
  return jsonify({
    'message':'Token has expired',
    'errorCode':'101'
  }),401
--------------- TOKEN NOT A VALID JWT -------------------
@jwt.invalid_token_loader
  This will notify whether the token provided is a valid JWT token or not

@jwt.invalid_token_loader
def invalid_token_callback(error):
  return jsonify ({
    'message':'Authentication failed',
    'error':'Invalid JWT'
  }), 401
--------------- TOKEN NOT provided -------------------
When user does not authenticate with any token  input

@jwt.unauthorized_loader
def unauthorized_loader_callback():
    return jsonify ({
    'message':'No access token provided'
    'error':'authorization_required'
    })
--------------- TOKEN NOT Fresh -------------------
When an endpoint needs a fresh token by provided token is not  fresh
@jwt.needs_fresh_token_loader
  def token_not_fresh_callback():
    return jsonify ({
    'message':'The token is not fresh'
    'error':'fresh_token_required'
    }), 401
--------------- TOKEN REVOKED & BLACKLIST-------------------
When a user token has been revoked access  or blacklisted

@jwt.revoked_token_loader
def revoked_token_callback():
  return jsonify ({
    'message':'The token has been revoked'
    'error':'token_revoked'
    }), 401

TOKEN BLACKLISTING
1. Create a file 'blacklist.py' and add the user id as set
  BLACKLIST = {2,3} #2 and 3 are blocked user ID

2. Enable blacklist in application. In app.py
  app.config['JWT_BLACKLIST_ENABLED'] = True --> enable blacklist
  app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh'] --> Include both access and refresh token in black list

3. Import blacklist file and decorate below function

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
  return decrypted_token['identity'] in BLACKLIST

4. When blacklist id is found JWT automatically goes to @jwt.revoked_token_loader
