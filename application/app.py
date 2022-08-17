from application.apis import covidcase_api
from flask import Flask


def create_app(app: Flask, config_name):
    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)
    app.register_blueprint(covidcase_api.blueprint, url_prefix='/covidcases')

    return app
