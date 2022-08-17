import os
from flask import Flask

from application.app import create_app

zen_app = Flask(__name__)
app = create_app(zen_app, os.environ["FLASK_CONFIG"])
