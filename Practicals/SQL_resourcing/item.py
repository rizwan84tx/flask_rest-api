import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    '''
    Class to get an item and run the Method accordingly
    '''
    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()

        if row:
            return {'item': {'name':row[0], 'price':row[1]}}
        return {'message':'Item not found'}, 404

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
