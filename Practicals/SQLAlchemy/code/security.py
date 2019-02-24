from models.user import UserModel
from werkzeug.security import safe_str_cmp #safe string comparision

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    '''
    Function unique to Flask-JWT - to know who is the current user logged in
    Takes in the the payload, that is content of JWT token and extracts the user identity from the payload
    The JWT payload: which is a dictionary, contains a key called identity, which is the user's id.
    In our code, if we want to have access to the current user, we can call jwt_identity() and it will return the current UserModel object.
    '''
    user_id = payload['identity']
    return UserModel.find_by_userid(user_id)
