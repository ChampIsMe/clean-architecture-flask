import json


class CovidCaseJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            # to_serialize = {
            #     "confirmed": o.confirmed,
            #     "recovered": o.recovered,
            #     "deaths": o.deaths,
            #     "country": str(o.country),
            #     "population": o.population,
            #     "sq_km_area": o.sq_km_area,
            #     "life_expectancy": str(o.life_expectancy),
            #     "elevation_in_meters": o.elevation_in_meters,
            #     "continent": str(o.continent),
            #     "abbreviation": str(o.abbreviation),
            #     "location": str(o.location),
            #     "capital_city": str(o.capital_city),
            #     "lat": str(o.lat),
            #     "long": str(o.long),
            #     "updated": str(o.updated)
            # }
            to_serialize = vars(o)
            return to_serialize
        except AttributeError as ex:  # pragma: no cover
            return super().default(o)
