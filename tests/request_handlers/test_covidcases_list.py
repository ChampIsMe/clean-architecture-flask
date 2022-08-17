import pytest
from unittest import mock

from backend.models.covidcase import CovidCase
from backend.api_handlers.covidcase_handler import covidcase_list_use_case
from backend.request_builders.covidcase_requests import build_covidcase_list_request
from backend.responses import ResponseTypes


@pytest.fixture
def domain_covidcases():
    covidcase_1 = CovidCase(
        confirmed=45,
        recovered=31,
        deaths=4,
        country="Kenya",
        population=64979540,
        sq_km_area=55150,
        life_expectancy="78.8",
        elevation_in_meters=375,
        continent="Africa",
        abbreviation="KE",
        location="East Africa",
        capital_city="Nairobi",
        lat="46.2276",
        long="2.2137",
        updated="2020/12/26 12:21:56+00"
    )

    covidcase_2 = CovidCase(
        confirmed=70,
        recovered=36,
        deaths=5,
        country="Nigeria",
        population=64979540,
        sq_km_area=55150,
        life_expectancy="78.8",
        elevation_in_meters=375,
        continent="Africa",
        abbreviation="NG",
        location='West Africa',
        capital_city="Abuja",
        lat="46.2276",
        long="2.2137",
        updated="2020/12/26 12:21:56+00"
    )

    covidcase_3 = CovidCase(
        confirmed=61,
        recovered=23,
        deaths=1,
        country="Uganda",
        population=64979540,
        sq_km_area=55150,
        life_expectancy="78.8",
        elevation_in_meters=375,
        continent="Africa",
        abbreviation="UG",
        location="East Africa",
        capital_city="Kampala",
        lat="46.2276",
        long="2.2137",
        updated="2020/12/26 12:21:56+00"
    )

    covidcase_4 = CovidCase(
        confirmed=46,
        recovered=12,
        deaths=1,
        country="Tanzania",
        population=64979540,
        sq_km_area=55150,
        life_expectancy="78.8",
        elevation_in_meters=375,
        continent="Africa",
        abbreviation="TZ",
        location="East Africa",
        capital_city="Dodoma",
        lat="46.2276",
        long="2.2137",
        updated="2020/12/26 12:21:56+00"
    )

    return [covidcase_1, covidcase_2, covidcase_3, covidcase_4]


def test_covidcase_list_without_parameters(domain_covidcases):
    repo = mock.Mock()
    repo.list.return_value = domain_covidcases
    request = build_covidcase_list_request()
    response = covidcase_list_use_case(repo, request)
    assert bool(response) is True
    repo.list.assert_called_with(filters=None)
    assert response.value == domain_covidcases


def test_covidcase_list_with_filters(domain_covidcases):
    repo = mock.Mock()
    repo.list.return_value = domain_covidcases
    qry_filters = {"country__eq": 5}
    request = build_covidcase_list_request(filters=qry_filters)
    response = covidcase_list_use_case(repo, request)
    assert bool(response) is True
    repo.list.assert_called_with(filters=qry_filters)
    assert response.value == domain_covidcases


def test_covidcase_list_handles_generic_error():
    repo = mock.Mock()
    repo.list.side_effect = Exception("Just an error message")
    request = build_covidcase_list_request(filters={})
    response = covidcase_list_use_case(repo, request)
    assert bool(response) is False
    assert response.value == {"type": ResponseTypes.SYSTEM_ERROR, "message": "Exception: Just an error message"}


