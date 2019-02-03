from flask import Flask, jsonify, request, render_template
# jsonify - for API to return data in JSON
# request - HTTP request from browser

app = Flask(__name__)
stores = [
    {
        'name': 'fitness',
        'items': [
            {
            'name': 'Whey Protein(5Lbs)',
            'price': 'INR 4,500',
            },
        ],
    },
]
@app.route('/')
def home():
    return render_template('index.html')

# ENDPOINT '/Store' -> API call are referenced to this ENDPOINT
# POST /store data :{name}
@app.route('/store', methods=['POST']) # ENDPOINT called only via POST
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items':[]
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>')   # http://127.0.0.1/2605/store/name
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})

# GET /Store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:,price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(store)
    return jsonify({'message': 'store not found'})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})

app.run(port=2605)
