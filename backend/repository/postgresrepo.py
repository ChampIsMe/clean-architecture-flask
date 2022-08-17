import json
import traceback

from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models import covidcase
from backend.repository.postgres_objects import Base, CovidCaseTable
from backend.serializers.covidcase import CovidCaseJsonEncoder

success_status_message = {'success': True}


class PostgresRepo:
    def __init__(self, configuration):
        connection_string = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            configuration["POSTGRES_USER"],
            configuration["POSTGRES_PASSWORD"],
            configuration["POSTGRES_HOSTNAME"],
            configuration["POSTGRES_PORT"],
            configuration["APPLICATION_DB"],
        )

        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine

    def make_session(self):
        DBSession = sessionmaker(bind=self.engine)
        # session = DBSession()
        return DBSession()

    async def savemultiplecases(self, caselist):
        with self.make_session() as session:
            # session.add_all(caselist)
            session.bulk_insert_mappings(CovidCaseTable, caselist)
            session.commit()
            session.close()

    def _create_covidcase_objects(self, results):
        return [
            covidcase.CovidCase(
                confirmed=q.confirmed,
                recovered=q.recovered,
                deaths=q.deaths,
                country=q.country,
                population=q.population,
                sq_km_area=q.sq_km_area,
                life_expectancy=q.life_expectancy,
                elevation_in_meters=q.elevation_in_meters,
                continent=q.continent,
                abbreviation=q.abbreviation,
                location=q.location,
                capital_city=q.capital_city,
                lat=q.lat,
                long=q.long,
                updated=q.updated
            )
            for q in results
        ]

    def list(self, filters=None):
        session = self.make_session()

        query = session.query(CovidCaseTable)
        if filters is None:
            return self._create_covidcase_objects(query.all())

        if "country__eq" in filters:
            query = query.filter(CovidCaseTable.country == filters["country__eq"])

        if "confirmed__eq" in filters:
            query = query.filter(CovidCaseTable.confirmed == filters["confirmed__eq"])

        if "confirmed__lt" in filters:
            query = query.filter(CovidCaseTable.confirmed < filters["confirmed__lt"])

        if "confirmed__gt" in filters:
            query = query.filter(CovidCaseTable.confirmed > filters["confirmed__gt"])
        caselist = self._create_covidcase_objects(query.all())
        session.commit()
        return caselist

    def createcase(self, covidcase_):
        object_ = CovidCaseTable(**covidcase_)
        with self.make_session() as session:
            session.add(object_)
            session.commit()
            session.close()

        with self.make_session() as session:
            # query = session.query(CovidCase).filter(CovidCase.country == covidcase_['country'])
            # query = session.query(CovidCase)
            query = session.query(CovidCaseTable).filter_by(country=covidcase_['country'])
            caselist = self._create_covidcase_objects(query.all())
            session.commit()
            session.close()

        # DBSession = sessionmaker(bind=self.engine)
        # session1 = DBSession()
        # session1.query(CovidCase).delete()
        # session1.commit()
        # session1.close()
        return vars(caselist[0])
