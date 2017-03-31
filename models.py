from app import db
from sqlalchemy.dialects.postgresql import JSON

ingredients_juices = db.Table('ingredients_juices',
    db.Column('juice_id', db.Integer, db.ForeignKey('juice.id')),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
)


class Juice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String())
    item_name = db.Column(db.String())
    calories = db.Column(db.Integer)
    servings_per_container = db.Column(db.Integer)
    serving_size_qty = db.Column(db.Integer)
    serving_size_unit = db.Column(db.String())
    ingredients = db.relationship('Ingredient', secondary=ingredients_juices, backref=db.backref('juices', lazy='dynamic'))

    def __init__(self, item_id, item_name, calories, servings_per_container, serving_size_qty, serving_size_unit):
        self.item_id = item_id
        self.item_name = item_name
        self.calories = calories
        self.servings_per_container = servings_per_container
        self.serving_size_qty = serving_size_qty
        self.serving_size_unit = serving_size_unit

    def __repr__(self):
        return '<item name {}>'.format(self.item_name)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<ingredient name {}>'.format(self.name)
