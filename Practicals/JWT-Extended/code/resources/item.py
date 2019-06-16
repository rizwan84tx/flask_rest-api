from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity, fresh_jwt_required
from models.item import ItemModel

class Item(Resource):
    '''
    Class to get an item and run the Method accordingly
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = "Field cannot be blank")

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}, 404

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

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'You need to an Admin to perform this'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    '''
    Class to list all Items - No input is required.
    Method will be self (no input)
    '''
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity() # VERIFY THAT USER IS LOGGED IN
        items = [item.json() for item in ItemModel.query.all()]
        if user_id:
            return {'items': items}, 200
        return {'items': "User not logged in"},200
