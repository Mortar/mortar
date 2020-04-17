from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient
from testfixtures import compare

from mortar import Mortar, Route, Mount, Router


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


def test_mount_router():
    async def user_list(request: Request):
        return [request.url_for('users:detail', username='foo')]

    async def user_detail(username: str):
        return {username: 'stuff'}

    router = Router(routes=[
        Route('/', user_list, name='list'),
        Route('/{username}', user_detail, name='detail'),
    ])

    async def root(request: Request):
        return {'users': request.url_for('users:list')}

    app = Mortar(routes=[
        Route("/", endpoint=root, name='root'),
        Mount('/users', name='users', router=router),
    ]).app()

    with TestClient(app) as client:
        compare(client.get("/").json(), expected={'users': 'http://testserver/users/'})
        compare(client.get("/users/").json(), expected=['http://testserver/users/foo'])
        compare(client.get("/users/foo").json(), expected={'foo': 'stuff'})


def test_mount_app():
    async def app(scope, receive, send):
        await PlainTextResponse('some content')(scope, receive, send)

    app = Mortar(routes=[Mount('/app', app=app)]).app()

    with TestClient(app) as client:
        compare(client.get("/app").content, expected=b'some content')
