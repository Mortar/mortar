from contextlib import asynccontextmanager

from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.testclient import TestClient
from testfixtures import compare, ShouldRaise
from testfixtures.mock import Mock, call

from mortar import Route, Mortar


class SampleMiddleware:
    def __init__(self, app, m, name):
        self.app = app
        self.m = getattr(m.middleware, name)

    async def __call__(self, scope, receive, send):
        self.m.before(scope['type'])
        await self.app(scope, receive, send)
        self.m.after(scope['type'])


def make_middleware(m, name):
    return Middleware(SampleMiddleware, m=m, name=name)


def make_func(m, name):
    async def func():
        getattr(m.func, name)()
    return func


def make_cm(m, name):

    @asynccontextmanager
    async def cm():
        m_ = getattr(m.context_manager, name)
        m_.start()
        try:
            yield
        except:
            m_.exception()
            raise
        else:
            m_.finish()

    return cm


def make_route(m, name, requires, path='/'):
    async def endpoint():
        getattr(m.endpoint, name)()
        return ['result for '+name]

    return Route(path, endpoint, requires=requires)


def test_full_lifecycle_normal():
    m = Mock()
    mortar = Mortar(
        lifespan=[make_func(m, 'func1'), make_cm(m, 'cm1'), make_func(m, 'func2')],
        middleware=[make_middleware(m, 'middleware1'), make_middleware(m, 'middleware2')],
        requires=[make_func(m, 'func3'), make_cm(m, 'cm2'), make_func(m, 'func4')],
        routes=[make_route(m, 'slash', requires=[make_cm(m, 'cm3'), make_func(m, 'func5')])],
    )
    app = mortar.app()

    compare(m.mock_calls, expected=[])

    with TestClient(app) as client:
        compare(m.mock_calls, expected=[
            call.func.func1(),
            call.context_manager.cm1.start(),
            call.func.func2(),
            call.middleware.middleware1.before('lifespan'),
            call.middleware.middleware2.before('lifespan'),
        ])
        m.reset_mock()

        response = client.get("/")
        compare(response.json(), expected=['result for slash'])
        compare(response.status_code, expected=200)

        compare(m.mock_calls, expected=[
            call.middleware.middleware1.before('http'),
            call.middleware.middleware2.before('http'),
            call.func.func3(),
            call.context_manager.cm2.start(),
            call.func.func4(),
            call.context_manager.cm3.start(),
            call.func.func5(),
            call.endpoint.slash(),
            call.context_manager.cm3.finish(),
            call.context_manager.cm2.finish(),
            call.middleware.middleware2.after('http'),
            call.middleware.middleware1.after('http'),
        ])

        m.reset_mock()

    compare(m.mock_calls, expected=[
        call.middleware.middleware2.after('lifespan'),
        call.middleware.middleware1.after('lifespan'),
        call.context_manager.cm1.finish(),
    ])


def test_full_lifecycle_exception():
    m = Mock()

    async def endpoint():
        m.endpoint.slash()
        raise Exception('boom!')

    mortar = Mortar(
        lifespan=[make_func(m, 'func1'), make_cm(m, 'cm1')],
        middleware=[make_middleware(m, 'middleware')],
        requires=[make_func(m, 'func2'), make_cm(m, 'cm2')],
        routes=[Route('/', endpoint, requires=[make_cm(m, 'cm3')])],
    )

    app = mortar.app()

    with TestClient(app) as client:
        compare(m.mock_calls, expected=[
            call.func.func1(),
            call.context_manager.cm1.start(),
            call.middleware.middleware.before('lifespan'),
        ])
        m.reset_mock()

        with ShouldRaise(Exception('boom!')):
            client.get("/")

        compare(m.mock_calls, expected=[
            call.middleware.middleware.before('http'),
            call.func.func2(),
            call.context_manager.cm2.start(),
            call.context_manager.cm3.start(),
            call.endpoint.slash(),
            call.context_manager.cm3.exception(),
            call.context_manager.cm2.exception(),
        ])

        m.reset_mock()

    compare(m.mock_calls, expected=[
        call.middleware.middleware.after('lifespan'),
        call.context_manager.cm1.finish(),
    ])


def test_multiple_routes_different_requires():
    m = Mock()
    mortar = Mortar(
        requires=[make_func(m, 'func1'), make_cm(m, 'cm1')],
        routes=[
            make_route(m, 'r1', requires=[make_cm(m, 'cm2'), make_func(m, 'func2')], path='/1'),
            make_route(m, 'r2', requires=[make_func(m, 'func3'), make_cm(m, 'cm3')], path='/2'),
        ],
    )
    app = mortar.app()

    with TestClient(app) as client:
        response = client.get("/1")
        compare(response.status_code, expected=200)
        compare(response.json(), expected=['result for r1'])

        compare(m.mock_calls, expected=[
            call.func.func1(),
            call.context_manager.cm1.start(),
            call.context_manager.cm2.start(),
            call.func.func2(),
            call.endpoint.r1(),
            call.context_manager.cm2.finish(),
            call.context_manager.cm1.finish(),
        ])

        m.reset_mock()

        response = client.get("/2")
        compare(response.status_code, expected=200)
        compare(response.json(), expected=['result for r2'])

        compare(m.mock_calls, expected=[
            call.func.func1(),
            call.context_manager.cm1.start(),
            call.func.func3(),
            call.context_manager.cm3.start(),
            call.endpoint.r2(),
            call.context_manager.cm3.finish(),
            call.context_manager.cm1.finish(),
        ])


def test_exception_handlers():

    m = Mock()

    class SampleException(Exception):
        pass

    def handler(request, exception):
        return JSONResponse({'exception': str(exception)}, status_code=500)

    async def endpoint():
        m.endpoint.slash()
        raise SampleException('boom!')

    mortar = Mortar(
        middleware=[make_middleware(m, 'middleware')],
        requires=[make_cm(m, 'cm1')],
        routes=[Route('/', endpoint, requires=[make_cm(m, 'cm2')])],
        exception_handlers={SampleException: handler}
    )
    app = mortar.app()

    with TestClient(app) as client:
        m.reset_mock()

        response = client.get("/")
        compare(response.status_code, expected=500)
        compare(response.json(), expected={'exception': 'boom!'})

        compare(m.mock_calls, expected=[
            call.middleware.middleware.before('http'),
            call.context_manager.cm1.start(),
            call.context_manager.cm2.start(),
            call.endpoint.slash(),
            call.context_manager.cm2.exception(),
            call.context_manager.cm1.exception(),
            call.middleware.middleware.after('http'),
        ])


def test_context_manager_swallows_exception():
    # this is probably a bad idea...
    async def endpoint():
        raise Exception('boom!')

    @asynccontextmanager
    async def bad():
        try:
            yield
        except:
            pass

    mortar = Mortar(
        requires=[bad],
        routes=[Route('/', endpoint)],
        debug=True,
    )
    app = mortar.app()

    with TestClient(app) as client:

        response = client.get("/")
        compare(response.status_code, expected=200)
        compare(response.json(), expected=None)
