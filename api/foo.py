from http import HTTPStatus

from aiohttp.web import json_response


async def post():
    return json_response(status=HTTPStatus.NOT_IMPLEMENTED)
