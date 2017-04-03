from flask import Flask, render_template, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
import json
import requests
import re


app = Flask(__name__)
admin = Admin(app, name='Juicy Juicy Data', template_mode='bootstrap3')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

from models import ingredients_juices, Ingredient, Juice
admin.add_view(ModelView(Juice, db.session))
admin.add_view(ModelView(Ingredient, db.session))

from assets import assets

@app.route('/', methods=['GET', 'POST'])
def index():
    # errors = []
    # total = {}
    #
    # payload = {
    #     "appId": "f5de3947",
    #     "appKey": "60fdc2f75e388c8018641eaa2d6f9e91",
    #     "query": "Juicy Juice",
    #     "offset": 0,
    #     "limit": 50,
    #     "filters": {
    #         "brand_id":"51db37d0176fe9790a899db2"
    #     }
    # }
    #
    # url = "https://api.nutritionix.com/v1_1/search/"
    # res = requests.post(url, json=payload).json()
    # total["total"] = res['total']
    #
    # total_calories = 0
    # total_ounces = 0

    juices_list = Juice.query.all()
    # for juice in juices_list:
    #     if juice.calories:
    #         total_calories += juice.calories
    #
    #     if juice.servings_per_container and juice.serving_size_qty and juice.serving_size_unit == "fl oz":
    #         total_ounces += juice.servings_per_container * juice.serving_size_qty
    #     elif juice.servings_per_container and juice.serving_size_qty and juice.serving_size_unit == "ml":
    #         ml_to_oz = juice.serving_size_qty * 0.033814
    #         total_ounces += juice.servings_per_container * ml_to_oz
    #
    #     avg_calories = total_calories / total_ounces
    #
    # calories_data = {
    #     "total_calories": total_calories,
    #     "total_ounces": total_ounces,
    #     "avg_calories_per_ounce": avg_calories,
    # }

    return render_template('index.html', juices=juices_list)

@app.route("/ingredients/<ingredient_id>")
def show_ingredient(ingredient_id):
    ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
    return render_template('ingredient-detail.html', ingredient=ingredient)

class Totals(Resource):
    def get(self):
        total_calories = 0
        total_ounces = 0
        payload = {
            "appId": "f5de3947",
            "appKey": "60fdc2f75e388c8018641eaa2d6f9e91",
            "query": "Juicy Juice",
            "offset": 0,
            "limit": 50,
            "filters": {
                "brand_id":"51db37d0176fe9790a899db2"
            }
        }

        url = "https://api.nutritionix.com/v1_1/search/"
        res = requests.post(url, json=payload).json()

        juices_list = Juice.query.all()
        for juice in juices_list:
            if juice.calories:
                total_calories += juice.calories

            if juice.servings_per_container and juice.serving_size_qty and juice.serving_size_unit == "fl oz":
                total_ounces += juice.servings_per_container * juice.serving_size_qty
            elif juice.servings_per_container and juice.serving_size_qty and juice.serving_size_unit == "ml":
                ml_to_oz = juice.serving_size_qty * 0.033814
                total_ounces += juice.servings_per_container * ml_to_oz

            avg_calories = total_calories / total_ounces

        totals = {
            "products": res['total'],
            "calories_data": {
                "total_calories": total_calories,
                "total_ounces": total_ounces,
                "avg_calories_per_ounce": avg_calories,
            }
        }

        return totals


api.add_resource(Totals, '/api/v1/totals')

if __name__ == '__main__':
    app.run()
