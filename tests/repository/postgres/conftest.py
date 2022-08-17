import sqlalchemy
import pytest

from backend.repository.postgres_objects import Base, CovidCaseTable


@pytest.fixture(scope="session")
def pg_session_empty(app_configuration):
    conn_str = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        app_configuration["POSTGRES_USER"],
        app_configuration["POSTGRES_PASSWORD"],
        app_configuration["POSTGRES_HOSTNAME"],
        app_configuration["POSTGRES_PORT"],
        app_configuration["APPLICATION_DB"],
    )
    engine = sqlalchemy.create_engine(conn_str)
    connection = engine.connect()

    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
    session = DBSession()

    yield session

    session.close()
    connection.close


@pytest.fixture(scope="session")
def pg_test_data():
    return [
        {
            "confirmed": 45,
            "recovered": 31,
            "deaths": 4,
            "country": "Kenya",
            "population": 64979540,
            "sq_km_area": 55150,
            "life_expectancy": "78.8",
            "elevation_in_meters": 375,
            "continent": "Africa",
            "abbreviation": "KE",
            "location": "East Africa",
            "capital_city": "Nairobi",
            "lat": "46.2276",
            "long": "2.2137",
            "updated": "2020/12/26 12:21:56+00"
        },
        {
            "confirmed": 46,
            "recovered": 32,
            "deaths": 5,
            "country": "Uganda",
            "population": 64949548,
            "sq_km_area": 551400,
            "life_expectancy": "78.8",
            "elevation_in_meters": 355,
            "continent": "Africa",
            "abbreviation": "UG",
            "location": "East Africa",
            "capital_city": "Kampala",
            "lat": "46.2276",
            "long": "2.2137",
            "updated": "2020/12/26 12:21:56+00"
        },
        {
            "confirmed": 60,
            "recovered": 33,
            "deaths": 2,
            "country": "Tanzania",
            "population": 64479548,
            "sq_km_area": 555500,
            "life_expectancy": "78.8",
            "elevation_in_meters": 365,
            "continent": "Africa",
            "abbreviation": "TZ",
            "location": "East Africa",
            "capital_city": 'Dodoma',
            "lat": "46.2276",
            "long": "2.2137",
            "updated": "2020/12/26 12:21:56+00"
        },
        {
            "confirmed": 76,
            "recovered": 34,
            "deaths": 3,
            "country": "Nigeria",
            "population": 64979548,
            "sq_km_area": 551500,
            "life_expectancy": "76.8",
            "elevation_in_meters": 375,
            "continent": "Africa",
            "abbreviation": "NG",
            "location": "Western Africa",
            "capital_city": "Abuja",
            "lat": "46.2276",
            "long": "2.2137",
            "updated": "2020/12/26 12:21:56+00"
        }
    ]


@pytest.fixture(scope="function")
def pg_session(pg_session_empty, pg_test_data):
    for r in pg_test_data:
        new_covidcase = CovidCaseTable(
            confirmed=r['confirmed'],
            recovered=r['recovered'],
            deaths=r['deaths'],
            country=r['country'],
            population=r['population'],
            sq_km_area=r['sq_km_area'],
            life_expectancy=r['life_expectancy'],
            elevation_in_meters=r['elevation_in_meters'],
            continent=r['continent'],
            abbreviation=r['abbreviation'],
            location=r['location'],
            capital_city=r['capital_city'],
            lat=r['lat'],
            long=r['long'],
            updated=r['updated']
        )
        pg_session_empty.add(new_covidcase)
        pg_session_empty.commit()

    yield pg_session_empty

    pg_session_empty.query(CovidCaseTable).delete()
