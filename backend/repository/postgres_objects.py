from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CovidCaseTable(Base):
    __tablename__ = "covidcase"

    id = Column(Integer, primary_key=True)

    confirmed = Column(Integer)
    recovered = Column(Integer)
    deaths = Column(Integer)
    country = Column(String, nullable=False)
    population = Column(Integer, nullable=True)
    sq_km_area = Column(Integer)
    life_expectancy = Column(String, nullable=True)
    elevation_in_meters = Column(String, nullable=True)
    continent = Column(String, nullable=False)
    abbreviation = Column(String, nullable=False)
    location = Column(String, nullable=False)
    capital_city = Column(String, nullable=True)
    lat = Column(String, nullable=False)
    long = Column(String, nullable=False)
    updated = Column(String, nullable=False)
