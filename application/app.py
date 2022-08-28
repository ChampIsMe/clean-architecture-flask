from application.apis import covidcase_api
from flask import Flask
from flask_cors import CORS, cross_origin
import logging

def create_app(app: Flask, config_name):
    CORS(app)
    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)
    app.register_blueprint(covidcase_api.blueprint, url_prefix='/covidcases')
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('flask_cors').level = logging.DEBUG

    return app
