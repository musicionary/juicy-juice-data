import json
import requests
import re
from flask_script import Command

from app import db
from models import ingredients_juices, Ingredient, Juice


class Seed(Command):
    """Seeds the database from the nutritionix api"""

    def create_payload(self, offset):
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
                "field": "item_name.sortable_na",
                "order": "desc"
            },
            "filters": {
                "brand_id": "51db37d0176fe9790a899db2"
            }
        }
        return payload

    def create_sample_database(self, offset):
        url = "https://api.nutritionix.com/v1_1/search/"
        headers = {'content-type': 'application/json'}

        res = requests.post(url, json=self.create_payload(offset)).json()

        for x in res['hits']:
            item_id = x['_id']
            item_name = x['fields']['item_name']
            calories = x['fields']['nf_calories']
            spc = x['fields']['nf_servings_per_container']
            ssq = x['fields']['nf_serving_size_qty']
            ssu = x['fields']['nf_serving_size_unit']
            ing_statement = x['fields']['nf_ingredient_statement']

            juice = None
            if Juice.query.filter_by(item_id=item_id).first() is None:
                juice = Juice(
                    item_id,
                    item_name,
                    calories,
                    spc,
                    ssq,
                    ssu
                )
                db.session.add(juice)
            else:
                juice = Juice.query.filter_by(item_id=item_id).first()

            if ing_statement is not None:
                ing_list = re.split(r',\s*(?![^()]*\))', ing_statement)
                for ing in ing_list:
                    ing_entry = None
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

    def build_database_entries(self):
        offset = 0
        total = {}
        url = "https://api.nutritionix.com/v1_1/search/"
        headers = {'content-type': 'application/json'}

        res = requests.post(url, json=self.create_payload(0)).json()
        total["total"] = res['total']

        while offset < total["total"]:
            self.create_sample_database(offset)
            offset += 50

    def run(self):
        self.build_database_entries()
