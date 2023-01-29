from __future__ import annotations

import aiohttp
from functional.config import test_settings
from functional.models.models import Response


async def make_get_request(
    end_of_url,
    query: str | None = None,
    page_number: int | str | None = None,
    page_size: int | str | None = None,
    sort: str | None = None,
    genre: str | None = None,
) -> Response:
    session = aiohttp.ClientSession()
    url = test_settings.service_url + "/api/v1/" + str(end_of_url)
    query_data = {}
    if query:
        query_data["query"] = str(query)
    if page_number:
        query_data["page[number]"] = page_number
    if page_size:
        query_data["page[size]"] = page_size
    if sort:
        query_data["sort"] = str(sort)
    if genre:
        query_data["filter[genre]"] = str(genre)

    async with session.get(url, params=query_data) as response:
        body = await response.json()
        status = response.status
    await session.close()
    return Response(body=body, status=status)
