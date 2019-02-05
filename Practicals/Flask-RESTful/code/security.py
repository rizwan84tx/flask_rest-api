from user import User
from werkzeug.security import safe_str_cmp #safe string comparision

users = [
    User(1, 'Rizwan', 'abc'),
]

username_mapping = {
    u.username: u for u in users #{"Rizwan":<user.User object at 0x000001...>}
}
userid_mapping = {
    u.id: u for u in users #{'1':<user.User object at 0x000001...>}
}

def authenticate(username, password):
    user = username_mapping.get(username, None) # .get retrieves the value for key 'username'. default - None (if no user found)
    if user and safe_str_cmp(user.password, password): # if user is not None and password matches
        return user

def identity(payload):
    '''
    Function unique to Flask-JWT - to know who is the current user logged in
    Takes in the the payload, that is content of JWT token and extracts the user identity from the payload
    The JWT payload: which is a dictionary, contains a key called identity, which is the user's id.
    In our code, if we want to have access to the current user, we can call jwt_identity() and it will return the current UserModel object.
    '''
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
