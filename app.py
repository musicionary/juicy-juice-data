from flask import Flask, render_template, request
# from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import os
import json
import requests
import re

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# api = Api(api)
db = SQLAlchemy(app)

from models import ingredients_juices, Ingredient, Juice

def create_payload(offset):
    payload = {
        "appId": "f5de3947",
        "appKey": "60fdc2f75e388c8018641eaa2d6f9e91",
        "query": "Juicy Juice",
        "fields": [
            "item_name",
            "brand_name",
            "nf_ingredient_statement",
            "nf_calories",
            "nf_servings_per_container",
            "nf_serving_size_qty",
            "nf_serving_size_unit"
        ],
        "offset": offset,
        "limit": 50,
        "sort": {
            "field":"item_name.sortable_na",
            "order":"desc"
        },
        "filters": {
            "brand_id":"51db37d0176fe9790a899db2"
        }
    }
    return payload

def create_sample_database(offset):
    url = "https://api.nutritionix.com/v1_1/search/"
    headers = {'content-type': 'application/json'}

    res = requests.post(url, json=create_payload(offset)).json()

    for x in res['hits']:
        item_id = x['_id']
        item_name = x['fields']['item_name']
        calories = x['fields']['nf_calories']
        spc = x['fields']['nf_servings_per_container']
        ssq = x['fields']['nf_serving_size_qty']
        ssu = x['fields']['nf_serving_size_unit']

        juice = Juice(
            item_id,
            item_name,
            calories,
            spc,
            ssq,
            ssu
        )
        db.session.add(juice)

        ing_statement = x['fields']['nf_ingredient_statement']
        if ing_statement is not None:
            ing_list = re.split(r',\s*(?![^()]*\))', ing_statement)
            for ing in ing_list:
                ing_entry = None
                import pdb; pdb.set_trace()
                if Ingredient.query.filter_by(name=ing).first() is None:
                    ing_entry = Ingredient(ing)
                    db.session.add(ing_entry)
                    db.session.commit()
                    juice.ingredients.append(ing_entry)
                else:
                    ing_entry = Ingredient.query.filter_by(name=ing).first()
                    juice.ingredients.append(ing_entry)


    db.session.commit()
    return res

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {"total": ""}
    total = {}

    offset = 0

    # url = "https://api.nutritionix.com/v1_1/search/"
    # headers = {'content-type': 'application/json'}
    #
    # res = requests.post(url, json=create_payload(0)).json()
    # total["total"] = res['total']

    create_sample_database(0)

    #results[x['_id']] = x['fields']
    # results = json.dumps(results)
    print(total)

    return render_template('index.html', errors=errors, results=total)

if __name__ == '__main__':
    app.run()
