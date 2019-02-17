from flask import Flask, request
from flask_restful import Resource, Api, reqparse #reqparse - parsing data from payload
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'rizwan' #key to excrypt the data
api = Api(app)

jwt =  JWT(app, authenticate, identity)

items = []

class Item(Resource):
    '''
    Class to get an item and run the Method accordingly
    '''
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda i: i['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda i: i['name'] == name, items), None):
            return {'message': "Item with name '{}' already exists!".format(name)}, 400
        data = request.get_json()
        item = { 'name': name, 'price': data['price'] }
        items.append(item)
        return item, 201 # 201 - status code: - Created

    def delete(self, name):
        global items # referring to global list 'items'
        items = list(filter(lambda i:i['name'] != name, items))
        return {'message':"Item deleted"}

    # This PUT method uses parser, to update only required data from payload
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
            type=float, #data type
            required=True, #data required
            help="Field cannot be blank"
        )
        data = parser.parse_args()
        item = next(filter(lambda i:i['name'] == name, items), None) # dict type
        if item is None:
            item = {'name': name,
                    'price': data['price']
                    }
            items.append(item)
        else:
            item.update(data) #update the item dict with input
        return item

class ItemList(Resource):
    '''
    Class to list all Items - No input is required.
    Method will be self (no input)
    '''
    def get(self):
        return {'items': items}

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

app.run(port=2605, debug=True)
