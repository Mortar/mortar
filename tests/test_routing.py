from starlette.requests import Request
from starlette.testclient import TestClient
from testfixtures import compare

from mortar import Mortar, Route


def test_no_required_resources():

    async def root():
        return {'count': 0}

    app = Mortar(routes=[Route("/", endpoint=root)]).app()

    with TestClient(app) as client:
        response = client.get("/")

    compare(response.status_code, expected=200)
    compare(response.json(), expected={'count': 0})


def test_route_methods():
    async def root():
        return {}

    app = Mortar(routes=[Route("/", endpoint=root, methods=['POST'])]).app()

    with TestClient(app) as client:
        response = client.get("/")
        compare(response.status_code, expected=405)
        compare(response.content, expected=b'Method Not Allowed')
        response = client.post("/")
        compare(response.status_code, expected=200)
        compare(response.json(), expected={})


def test_route_name():

    async def root(request: Request):
        return {'entity': request.url_for('entity')}

    async def entity():
        return {'foo': 'bar'}

    app = Mortar(routes=[
        Route("/", endpoint=root, name='root'),
        Route("/entity", endpoint=entity, name='entity'),
    ]).app()

    with TestClient(app) as client:
        response = client.get("/")
        result = response.json()
        compare(result, expected={'entity': 'http://testserver/entity'})
        response = client.get(result['entity'])
        compare(response.json(), expected={'foo': 'bar'})
