import json

import os
from flask import Flask

from application.app import create_app

from backend.models.covidcase import CovidCase

covidcase_dict = {
    "confirmed": 2604595,
    "recovered": 195365,
    "deaths": 62548,
    "country": "MyCountry",
    "population": 64979548,
    "sq_km_area": 551500,
    "life_expectancy": "78.8",
    "elevation_in_meters": 375,
    "continent": "Europe",
    "abbreviation": "FR",
    "location": "Western Europe",
    "capital_city": "Paris",
    "lat": "46.2276",
    "long": "2.2137",
    "updated": "2020/12/26 12:21:56+00"
}

covidcases = [CovidCase.from_dict(covidcase_dict)]
success_status_message = {'success': True}


def test_get():
    zen_app = Flask(__name__)
    create_app(zen_app, os.environ["FLASK_CONFIG"])
    client = zen_app.test_client()

    http_response = client.get("/covidcases/listcases")
    response_data = http_response.data.decode("UTF-8")
    loaded = json.loads(response_data)
    countries = [item['country'] for item in loaded]
    assert all(elem['country'] in countries for elem in loaded)
    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"


def test_create_covidcase():
    zen_app = Flask(__name__)
    create_app(zen_app, os.environ["FLASK_CONFIG"])
    client = zen_app.test_client()
    headers = {'content-type': 'application/json'}
    http_response = client.post("/covidcases/savecases", json=covidcase_dict, headers=headers)
    response_data = json.loads(http_response.data.decode("UTF-8"))
    assert set(response_data) == set(covidcase_dict)
    assert response_data['country'] == covidcase_dict['country']
    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"


def test_get_response_failures():
    zen_app = Flask(__name__)
    create_app(zen_app, os.environ["FLASK_CONFIG"])
    client = zen_app.test_client()
    http_response = client.get("/covidcases/listcases?dummy_request_string=123")
    assert http_response.status_code in [400, 404, 500]


def test_get_with_filters():
    zen_app = Flask(__name__)
    create_app(zen_app, os.environ["FLASK_CONFIG"])
    client = zen_app.test_client()
    http_response = client.get("/covidcases/listcases?confirmed__gt=2604594&confirmed__lt=2604596")
    response_data = json.loads(http_response.data.decode("UTF-8"))
    assert any([item['country'] == 'MyCountry' for item in response_data])
    assert http_response.status_code == 200
    assert http_response.mimetype == "application/json"
