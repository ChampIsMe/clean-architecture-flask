from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from jsonschema import validate

# "null", "boolean", "object", "array", "number", or "string"
from backend.responses import ResponseFailure, ResponseTypes

numberOrString = {'anyOf': [{'type': 'number'}, {'type': 'string', "pattern": "^[0-9]+$"}]}
nullable = {'anyOf': [{'type': ['number', 'null']}, {'type': 'string', "pattern": "^[0-9]+$"}]}
covidcase_post = {
    "type": 'object',
    'properties': {
        "confirmed": numberOrString,
        "recovered": numberOrString,
        "deaths": numberOrString,
        "country": {'type': ['string', 'null']},
        "population": nullable,
        "sq_km_area": numberOrString,
        "life_expectancy": {'type': ['string', 'null']},
        "elevation_in_meters": {'type': ['string', 'null', 'number']},
        "continent": {'type': 'string'},
        "abbreviation": {'type': 'string'},
        "location": {'type': 'string'},
        "capital_city": {'type': ['string', 'null']},
        "lat": {'type': 'string'},
        "long": {'type': 'string'},
        "updated": {'type': 'string'}
    },
    "additionalProperties": False
}

covidcase_get = {
    "type": 'object',
    'properties': {
        "country__eq": {'type': 'string'},
        "confirmed__eq": numberOrString,
        "confirmed__lt": numberOrString,
        "confirmed__gt": numberOrString,
        "page": numberOrString,
        "limit": numberOrString
    },
    "additionalProperties": False
}


class CovidCasePost(Inputs):
    json = [JsonSchema(schema=covidcase_post)]


class CovidCaseGet(Inputs):
    json = [JsonSchema(schema=covidcase_get)]


def validate_covidcase_post(request):
    try:
        inputs = CovidCasePost(request)
        if inputs.validate():
            return None
        else:
            response = ResponseFailure(ResponseTypes.PARAMETERS_ERROR, inputs.errors)
            return response
    except Exception as ex:
        # Fallback to validator when flask-input error occurs in production with python version > 3.8
        try:
            validate(instance=request.get_json(), schema=covidcase_post)
            return None
        except Exception as ex:
            response = ResponseFailure(ResponseTypes.PARAMETERS_ERROR, vars(ex)['message'])
            return response


def validate_covidcase_get(request):
    try:
        validate(instance=request.args, schema=covidcase_get)
        return None
    except Exception as ex:
        response = ResponseFailure(ResponseTypes.PARAMETERS_ERROR, vars(ex)['message'])
        return response
