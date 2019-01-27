from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from marshmallow import ValidationError

from model import stock_schema
from utils import get_config


config = get_config()
app = Flask(__name__)
app.config['MONGO_URI'] = config['mongourl']
mongo = PyMongo(app)

def gen_recurs_update(data_dict, prefix=''):
    result = {}
    for k, v in data_dict.items():
        if isinstance(v, dict):
            result.update(gen_recurs_update(v, f'{prefix}{k}.'))
        else:
            result[f'{prefix}{k}'] = v
    return result

@app.route('/stocks/<symbol>', methods=['GET'])
def get_stock(symbol):
    stock = mongo.db.companies.find_one_or_404({'symbol': symbol.upper()})
    stock['id'] = str(stock.pop('_id'))
    return jsonify(stock)

@app.route('/stocks', methods=['GET'])
def get_stocks():
    stock_objects = mongo.db.companies.find({}, {'symbol': 1})
    stocks = []
    for stock in stock_objects:
        stock['id'] = str(stock.pop('_id'))
        stocks.append(stock)
    return jsonify(stocks)

@app.route('/stocks/<symbol>', methods=['POST'])
def add_stock(symbol):
    content = request.json
    symbol_inner = content.get('symbol')
    if not content or not symbol_inner or symbol.upper() != symbol_inner.upper():
        return ('symbol: not a valid item', 400)

    try:
        stock_schema.load(content)
    except ValidationError as e:
        return (str(e), 400)

    stock = mongo.db.companies.find_one({'symbol': symbol.upper()})
    if stock:
        return (f'symbol "{symbol}": already exists', 400)

    content['symbol'] = content['symbol'].upper()
    stock_new = mongo.db.companies.insert_one(content)
    # TODO: logging
    return ('', 201)

@app.route('/stocks', methods=['POST'])
def add_stocks():
    content = request.json
    if not content or not isinstance(content, list):
        return ('expect an array', 400)

    for item in content:
        try:
            stock_schema.load(item)
        except ValidationError as e:
            return (str(e), 400)

        stock = mongo.db.companies.find_one({'symbol': item['symbol'].upper()})
        if stock:
            symbol = item['symbol']
            return (f'symbol "{symbol}": already exists', 400)

    for item in content:
        item['symbol'] = item['symbol'].upper()
        stock_new = mongo.db.companies.insert_one(item)
        # TODO: logging
    return ('', 201)

@app.route('/stocks/<symbol>', methods=['PUT'])
def update_stock(symbol):
    stock = mongo.db.companies.find_one_or_404({'symbol': symbol.upper()})
    if not stock:
        return ('', 404)

    content = request.json
    if not content:
        return ('Wrong content', 400)

    stock_up = mongo.db.companies.find_one_and_update(
        {'_id': stock['_id']},
        {'$set': gen_recurs_update(content)},
    )
    # TODO: logging
    return ('', 200)

@app.route('/stocks/<symbol>', methods=['DELETE'])
def delete_stock(symbol):
    stock = mongo.db.companies.find_one_or_404({'symbol': symbol.upper()})
    stock_del = mongo.db.companies.delete_one({'_id': stock['_id']})
    # TODO: logging
    return ('', 200)

if __name__ == '__main__':
    app.run(debug=config['debug'])
