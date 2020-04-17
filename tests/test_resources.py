from mush import Context, ContextError, returns, requires
from starlette.requests import Request
from starlette.testclient import TestClient
from testfixtures import compare, ShouldRaise

from mortar import Mortar, Route


def test_lifespan_provides_resources():

    @returns('resource')
    def make_resource():
        return 'the resource'

    @requires('resource')
    async def root(resource):
        return resource

    app = Mortar(
        lifespan=[make_resource],
        routes=[Route("/", endpoint=root)]
    ).app()

    with TestClient(app) as client:
        response = client.get("/")
        compare(response.json(), expected='the resource')


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


def test_route_requires_singular():

    async def root(context: Context):
        return {k: v for (k, v) in context._store.items() if k is not Request}

    mortar = Mortar(routes=[Route("/", endpoint=root, requires='foo')])
    app = mortar.app()

    with TestClient(app) as client:
        with ShouldRaise(ContextError):
            client.get("/")

        mortar.context.add('value', provides='foo')

        response = client.get("/")
        compare(response.json(), expected={'foo': 'value'})


def test_route_requires_multiple():

    async def root(context: Context):
        return {k: v for (k, v) in context._store.items() if k is not Request}

    mortar = Mortar(routes=[Route("/", endpoint=root, requires=['foo', 'bar'])])
    app = mortar.app()

    with TestClient(app) as client:
        mortar.context.add('value1', provides='foo')
        mortar.context.add('value2', provides='bar')

        response = client.get("/")
        compare(response.json(), expected={'foo': 'value1', 'bar': 'value2'})


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
