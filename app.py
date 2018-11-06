import uuid
from http import HTTPStatus
from json import JSONDecodeError

import connexion
from aiohttp import web
from aiohttp.web import json_response
from connexion.resolver import RestyResolver


@web.middleware
async def log_middleware(request, handler):
    print('ENTER: log_middleware')
    try:
        req_body = await request.json() if request.has_body else None
    except JSONDecodeError as e:
        return json_response(data='Invalid request parameters.', status=HTTPStatus.BAD_REQUEST)

    req_id = str(uuid.uuid4())

    print({'message': req_id,
           'type': 'request',
           'req_id': req_id,
           'body': req_body,
           'cookies': dict(request.cookies),
           'content-type': request.content_type,
           'content-length': request.content_length,
           'headers': dict(request.headers),
           'method': request.method,
           'query': dict(request.query),
           'url': str(request.url)})

    response = await handler(request)

    print({'message': req_id,
           'type': 'response',
           'req_id': req_id,
           'body': response.text,
           'cookies': dict(response.cookies),
           'content_type': response.content_type,
           'content_length': response.content_length,
           'headers': dict(response.headers),
           'status_code': response.status})

    return response


app = connexion.AioHttpApp('__main__',
                           specification_dir='swagger/',
                           options={'middlewares': [log_middleware]})  # XXX: Remove log_middleware and it works
app.add_api('api.spec.yaml',
            resolver=RestyResolver('api'),
            validate_responses=True,
            strict_validation=True,
            pass_context_arg_name='request')


application = app.app

app.run(port=int(8080))
