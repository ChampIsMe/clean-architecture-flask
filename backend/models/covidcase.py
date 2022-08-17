import dataclasses
import json


@dataclasses.dataclass
class CovidCase:
    confirmed: int
    recovered: int
    deaths: int
    country: str
    population: int
    sq_km_area: int
    life_expectancy: str
    elevation_in_meters: str
    continent: str
    abbreviation: str
    location: str
    capital_city: str
    lat: str
    long: str
    updated: str

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
