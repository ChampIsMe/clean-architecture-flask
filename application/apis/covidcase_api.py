import os
import json
from backend.validation.schemas import validate_covidcase_post, validate_covidcase_get
from flask import Blueprint, request, Response, jsonify

from backend.repository.postgresrepo import PostgresRepo
from backend.api_handlers.covidcase_handler import save_case_use_case, covidcase_list_use_case
from backend.serializers.covidcase import CovidCaseJsonEncoder
from backend.request_builders.covidcase_requests import build_covidcase_list_request, build_save_covidcase_request, CovidCaseRequest
from backend.responses import ResponseTypes, build_response_from_invalid_request, ResponseFailure

blueprint = Blueprint("covidcase", __name__)

STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
}

postgres_configuration = {
    "POSTGRES_USER": os.environ["POSTGRES_USER"],
    "POSTGRES_PASSWORD": os.environ["POSTGRES_PASSWORD"],
    "POSTGRES_HOSTNAME": os.environ["POSTGRES_HOSTNAME"],
    "POSTGRES_PORT": os.environ["POSTGRES_PORT"],
    "APPLICATION_DB": os.environ["APPLICATION_DB"],
}


@blueprint.route("/listcases", methods=["GET"])
def covidcase_list():
    error_response = validate_covidcase_get(request)
    if error_response is not None:
        resp = json.dumps(error_response.value, cls=CovidCaseJsonEncoder)
        return jsonify(json.loads(resp)), STATUS_CODES[error_response.type]

    qrystr_params = {"filters": {}}

    for arg, values in request.args.items():
        if arg.startswith("filter_"):
            qrystr_params["filters"][arg.replace("filter_", "")] = values
        else:
            qrystr_params["filters"][arg] = values
    request_object = build_covidcase_list_request(filters=qrystr_params["filters"])
    repo = PostgresRepo(postgres_configuration)
    response = covidcase_list_use_case(repo, request_object)
    resp = json.dumps(response.value, cls=CovidCaseJsonEncoder)
    return jsonify(json.loads(resp)), STATUS_CODES[response.type]


@blueprint.route("/savecases", methods=["POST"])
def savecase():
    error_response = validate_covidcase_post(request)
    if error_response is not None:
        resp = json.dumps(error_response.value, cls=CovidCaseJsonEncoder)
        return jsonify(json.loads(resp)), STATUS_CODES[error_response.type]

    datastring = request.get_json()
    request_object = build_save_covidcase_request(datastring)
    repo = PostgresRepo(postgres_configuration)
    response = save_case_use_case(repo, request_object)
    return jsonify(response.value), STATUS_CODES[response.type]
