from flask_assets import Bundle, Environment
from app import app

bundles = {
    "css": Bundle(
        "main.css",
        output="build/styles.css",
        filters="cssmin",
    ),

}


assets = Environment(app)
assets.register(bundles)
