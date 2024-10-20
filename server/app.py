#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_formatted =  []
    for bakery in bakeries:
        bakery_formatted = {'id': bakery.id,
                            'name': bakery.name,
                            'created_at': bakery.created_at,
                            'updated_at': bakery.updated_at}
        bakeries_formatted.append(bakery_formatted)
    
    return make_response(bakeries_formatted, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_formatted = {'id': bakery.id,
                            'name': bakery.name,
                            'created_at': bakery.created_at,
                            'updated_at': bakery.updated_at}
    return make_response(bakery_formatted, 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_formatted = []
    for good in baked_goods:
        baked_goods_formatted.append({'id': good.id,
                                        'name': good.name,
                                        'price': good.price,
                                        'created_at': good.created_at,
                                        'updated_at': good.updated_at})
    return make_response(baked_goods_formatted, 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    baked_good_formatted = {'id': good.id,
                            'name': good.name,
                            'price': good.price,
                            'created_at': good.created_at,
                            'updated_at': good.updated_at}
    return make_response(baked_good_formatted, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
