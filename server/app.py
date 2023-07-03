from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# Existing routes...

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    name = data.get('name')
    price = data.get('price')
    bakery_id = data.get('bakery_id')

    if not name or not price or not bakery_id:
        return make_response(jsonify({'error': 'Incomplete data provided.'}), 400)

    bakery = Bakery.query.get(bakery_id)
    if not bakery:
        return make_response(jsonify({'error': 'Bakery not found.'}), 404)

    baked_good = BakedGood(name=name, price=price, bakery=bakery)
    db.session.add(baked_good)
    db.session.commit()

    return make_response(jsonify(baked_good.to_dict()), 201)


@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    data = request.form
    name = data.get('name')

    bakery = Bakery.query.get(id)
    if not bakery:
        return make_response(jsonify({'error': 'Bakery not found.'}), 404)

    if name:
        bakery.name = name

    db.session.commit()

    return make_response(jsonify(bakery.to_dict()), 200)


@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if not baked_good:
        return make_response(jsonify({'error': 'Baked Good not found.'}), 404)

    db.session.delete(baked_good)
    db.session.commit()

    return make_response(jsonify({'message': 'Baked Good deleted successfully.'}), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
