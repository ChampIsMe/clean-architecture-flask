import uuid
from backend.models.covidcase import CovidCase


def test_covidcase_model_init():
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
    # Testing just a few
    assert covidcase.confirmed == 2604595
    assert covidcase.recovered == 195365
    assert covidcase.deaths == 62548
    assert covidcase.country == "France"
    assert covidcase.population == 64979548


def test_covidcase_model_from_dict():
    init_dict = {
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
    }

    covidcase = CovidCase.from_dict(init_dict)

    # Testing just a few
    assert covidcase.confirmed == 2604595
    assert covidcase.recovered == 195365
    assert covidcase.deaths == 62548
    assert covidcase.country == "France"
    assert covidcase.population == 64979548


def test_covidcase_model_to_dict():
    init_dict = {
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
    }

    covidcase = CovidCase.from_dict(init_dict)
    assert covidcase.to_dict() == init_dict


def test_covidcase_model_comparison():
    init_dict = {
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
    }

    covidcase1 = CovidCase.from_dict(init_dict)
    covidcase2 = CovidCase.from_dict(init_dict)

    assert covidcase1 == covidcase2
