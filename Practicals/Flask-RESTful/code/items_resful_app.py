from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'rizwan' #key to excrypt the data
api = Api(app)

jwt =  JWT(app, authenticate, identity)
# JWT creates a new endpoint '/auth'.
# When you call /auth, we send username and password
# JWT get the username and password and sends it to authenticate func.
#   authenticate function returns the user as 'JWTtoken''
# JWT then sends 'JWTtoken' is sent to identity func and gets the correct user for that token.

items = []

class Item(Resource):
    '''
    Class to get an item and run the Method accordingly
    '''
    @jwt_required() # user needs to be authenticated to call this endpoint
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        #return {'item': None}, 404 # 404 - status code : not found
        item = next(filter(lambda i: i['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404
        # next - Gives 1st item matches  the requirement, if item not available it will error out
        # if there are no items, then using 'None' does not cause error

    def post(self, name):
        if next(filter(lambda i: i['name'] == name, items), None):
            return {'message': "Item with name '{}' already exists!".format(name)}, 400

        data = request.get_json() # will give error is data payload is not json
        # request.get_json(force=True): will process the text, even if the header is not in json format - not recommended
        # request.get_json(silent=True): will return none and does not get an error if payload is not a json
        item = { 'name': name, 'price': data['price'] }
        items.append(item)
        return item, 201 # 201 - status code: - Created

class ItemList(Resource):
    '''
    Class to list all Items - No input is required.
    Method will be self (no input)
    '''
    def get(self):
        return {'items': items}

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

app.run(port=2605, debug=True)
