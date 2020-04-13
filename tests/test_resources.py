from mush import Context
from starlette.requests import Request
from starlette.testclient import TestClient
from testfixtures import compare

from mortar import Mortar, Route


def test_wants_request():

    async def root(request: Request):
        return {'count': request.query_params['count']}

    app = Mortar(routes=[Route("/", endpoint=root)], debug=True).app()

    with TestClient(app) as client:
        response = client.get("/?count=1")
        compare(response.json(), expected={'count': '1'})
        response = client.get("/?count=2")
        compare(response.json(), expected={'count': '2'})


def test_synchronous_handler_gets_synchronous_context():

    def root(context: Context):
        return {'count': context.get(Request).query_params['count']}

    app = Mortar(routes=[Route("/", endpoint=root)], debug=True).app()

    with TestClient(app) as client:
        response = client.get("/?count=1")
        compare(response.json(), expected={'count': '1'})


def test_default_resolver():

    async def root(path_param='bad', request_param='bad', missing_param='missing_good'):
        return {'path_param': path_param,
                'request_param': request_param,
                'missing_param': missing_param}

    app = Mortar(routes=[Route("/{path_param}", endpoint=root)]).app()

    with TestClient(app) as client:
        response = client.get("/path_good?path_param=bad&request_param=request_good")
        compare(response.json(), expected={
            'path_param': 'path_good',
            'request_param': 'request_good',
            'missing_param': 'missing_good',
        })


def test_default_resolver_with_type():

    async def root(param1: int, param2: int = 2):
        return {'param1': param1, 'param2': param2}

    app = Mortar(routes=[Route("/", endpoint=root)]).app()

    with TestClient(app) as client:
        response = client.get("/?param1=1")
        compare(response.json(), expected={'param1': 1, 'param2': 2})
