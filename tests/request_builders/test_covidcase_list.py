import json
import os

import pytest

from flask import Flask

from application.app import create_app
from backend.request_builders.covidcase_requests import build_covidcase_list_request


def test_build_covidcase_list_request_without_parameters():
    request = build_covidcase_list_request()
    assert request.filters is None
    assert bool(request) is True


def test_build_covidcase_list_request_with_empty_filters():
    request = build_covidcase_list_request({})
    assert request.filters == {}
    assert bool(request) is True


def test_build_covidcase_list_request_with_invalid_filters_parameter():
    zen_app = Flask(__name__)
    create_app(zen_app, os.environ["FLASK_CONFIG"])
    client = zen_app.test_client()
    http_response = client.get("/covidcases/listcases?filters=5")
    assert http_response.status_code == 400
    response_data = json.loads(http_response.data.decode("UTF-8"))
    assert 'Additional properties are not allowed' in response_data['message']



@pytest.mark.parametrize("key", ["country__eq", "confirmed__eq", "confirmed__lt", "confirmed__gt"])
def test_build_covidcase_list_request_accepted_filters(key):
    filters = {key: 1}
    request = build_covidcase_list_request(filters=filters)
    assert request.filters == filters
    assert bool(request) is True


@pytest.mark.parametrize("key", ["country__lx", "country__gx"])
def test_build_covidcase_list_request_rejected_filters(key):
    zen_app = Flask(__name__)
    create_app(zen_app, os.environ["FLASK_CONFIG"])
    client = zen_app.test_client()
    http_response = client.get("/covidcases/listcases?filter_country__lx=2604594&filter_country__gx=2604596")
    assert http_response.status_code == 400
    response_data = json.loads(http_response.data.decode("UTF-8"))
    assert 'Additional properties are not allowed' in response_data['message']
