import asyncio
from backend.models.covidcase import CovidCase

import aiohttp

from backend.repository.postgresrepo import PostgresRepo
from backend.request_builders.covidcase_requests import CovidCaseRequest
from backend.responses import (ResponseSuccess, ResponseFailure, ResponseTypes, build_response_from_invalid_request)


def covidcase_list_use_case(repo: PostgresRepo, request: CovidCaseRequest):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        covidcases = repo.list(filters=request.filters)
        if len(covidcases) == 0 or len(covidcases) >= 6:
            asyncio.run(loadcases(repo))
            covidcases = repo.list(filters=request.filters)

        return ResponseSuccess(covidcases)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)


async def loadcases(repo):
    async with aiohttp.ClientSession() as session:
        url = 'https://covid-api.mmediagroup.fr/v1/cases'
        r = await session.get(url, ssl=False)
        data = await r.json()
        countries = data.keys()
        ccase = CovidCase(1, 1, 1, '1', 1, 1, '1', '1', '1', '1', '1', '1', '1', '1', '1')
        casedict = vars(ccase)
        # For test purposes, I'm using cases with all the attributes of the DB model I created
        iterator = map(lambda country: {k: v for k, v in data[country]['All'].items() if k in casedict}, [country for country in countries if (set(vars(ccase)) <= set(data[country]['All']))])
        cases = list(iterator)
        # models = [CovidCaseTable(**item) for item in cases]
        # await repo.savemultiplecases(models)
        await repo.savemultiplecases(cases)


def save_case_use_case(repo, request: CovidCaseRequest):
    if not request:
        return build_response_from_invalid_request(request)
    try:
        result = repo.createcase(request.payload)
        return ResponseSuccess(result)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
