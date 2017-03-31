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

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    total = {}

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
    headers = {'content-type': 'application/json'}

    res = requests.post(url, json=payload).json()
    total["total"] = res['total']


    return render_template('index.html', errors=errors, results=total)

if __name__ == '__main__':
    app.run()
