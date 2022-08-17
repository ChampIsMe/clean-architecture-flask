import pytest
from backend.repository import postgresrepo

pytestmark = pytest.mark.integration


def test_repository_list_without_parameters(app_configuration, pg_session, pg_test_data):
    repo = postgresrepo.PostgresRepo(app_configuration)
    repo_covidcases = repo.list()
    assert set([r["country"] for r in pg_test_data]).issubset(set([r.country for r in repo_covidcases]))


def test_repository_list_with_country_equal_filter(app_configuration, pg_session, pg_test_data):
    repo = postgresrepo.PostgresRepo(app_configuration)
    repo_covidcases = repo.list(filters={"country__eq": "Kenya"})
    assert len(repo_covidcases) == 1
    assert repo_covidcases[0].country == "Kenya"


def test_repository_list_with_confirmed_equal_filter(app_configuration, pg_session, pg_test_data):
    repo = postgresrepo.PostgresRepo(app_configuration)
    repo_covidcases = repo.list(filters={"confirmed__eq": 60})
    assert len(repo_covidcases) == 1
    assert repo_covidcases[0].country == "Tanzania"


def test_repository_list_with_confirmed_less_than_filter(app_configuration, pg_session, pg_test_data):
    repo = postgresrepo.PostgresRepo(app_configuration)
    repo_covidcases = repo.list(filters={"confirmed__lt": 60})
    assert len(repo_covidcases) == 2
    assert set([r.country for r in repo_covidcases]) == {'Kenya', 'Uganda'}


def test_repository_list_with_confirmed_greater_than_filter(app_configuration, pg_session, pg_test_data):
    repo = postgresrepo.PostgresRepo(app_configuration)
    repo_covidcases = repo.list(filters={"confirmed__gt": 48})
    assert len(repo_covidcases) == 2
    assert set([r.country for r in repo_covidcases]) == {"Tanzania", "Nigeria"}


def test_repository_list_with_confirmed_between_filter(app_configuration, pg_session, pg_test_data):
    repo = postgresrepo.PostgresRepo(app_configuration)
    repo_covidcases = repo.list(filters={"confirmed__lt": 66, "confirmed__gt": 48})
    assert len(repo_covidcases) == 1
    assert repo_covidcases[0].country == "Tanzania"
