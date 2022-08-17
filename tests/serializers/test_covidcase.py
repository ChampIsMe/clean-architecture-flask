import json

from backend.serializers.covidcase import CovidCaseJsonEncoder
from backend.models.covidcase import CovidCase


def test_serialize_domain_covidcase():
    covidcase = CovidCase(
        confirmed=2604595,
        recovered=195365,
        deaths=62548,
        country="France",
        population=64979548,
        sq_km_area=551500,
        life_expectancy="78.8",
        elevation_in_meters=375,
        continent="Europe",
        abbreviation="FR",
        location="Western Europe",
        capital_city="Paris",
        lat="46.2276",
        long="2.2137",
        updated="2020/12/26 12:21:56+00"
    )

    expected_json = f"""
        {{
            "confirmed": 2604595,
            "recovered": 195365,
            "deaths": 62548,
            "country": "France",
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
        }}
    """

    json_covidcase = json.dumps(covidcase, cls=CovidCaseJsonEncoder)

    assert json.loads(json_covidcase) == json.loads(expected_json)
