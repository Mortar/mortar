from mush import Context, ContextError, returns, requires, Value
from mush.tests.helpers import no_threads
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient
from testfixtures import compare, ShouldRaise

from mortar import Mortar, Route, Router, Mount
from mortar.resolvers import FromRequest


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


async def context_contents(context: Context):
    return {k: v for (k, v) in context._store.items() if k is not Request}


def test_mortar_requires():

    mortar = Mortar(routes=[Route("/", endpoint=context_contents)], requires=Value('bar'))
    app = mortar.app()

    with TestClient(app) as client:
        with ShouldRaise(ContextError):
            client.get("/")

        mortar.context.add('value', provides='bar')

        response = client.get("/")
        compare(response.json(), expected={'bar': 'value'})


def test_mortar_requires_request_and_provided_by_tween():

    @requires(Value('bar'), FromRequest('bob'))
    @returns('baz')
    def make_baz(bar: str, bob: str):
        return 'baz'+bar+bob

    mortar = Mortar(tweens=[make_baz],
                    requires=(Value('bar'), Value('baz')),
                    routes=[Route("/", endpoint=context_contents)])
    app = mortar.app()

    with TestClient(app) as client:
        mortar.context.add('value', provides='bar')

        response = client.get("/?bob=bobvalue")
        compare(response.json(), expected={'bar': 'value',
                                           'baz': 'bazvaluebobvalue'})


def test_route_requires_singular():

    mortar = Mortar(routes=[Route("/", endpoint=context_contents, requires=Value('foo'))])
    app = mortar.app()

    with TestClient(app) as client:
        with ShouldRaise(ContextError):
            client.get("/")

        mortar.context.add('value', provides='foo')

        response = client.get("/")
        compare(response.json(), expected={'foo': 'value'})


def test_route_requires_multiple():

    mortar = Mortar(routes=[Route("/",
                                  endpoint=context_contents,
                                  requires=[Value('foo'), Value('bar')])])
    app = mortar.app()

    with TestClient(app) as client:
        mortar.context.add('value1', provides='foo')
        mortar.context.add('value2', provides='bar')

        response = client.get("/")
        compare(response.json(), expected={'foo': 'value1', 'bar': 'value2'})


def test_requires_no_threads_if_all_async():

    mortar = Mortar(routes=[Route("/", endpoint=context_contents, requires=Value('foo'))])
    app = mortar.app()

    with TestClient(app) as client:
        mortar.context.add('value', provides='foo')

        with no_threads():
            response = client.get("/")

        compare(response.json(), expected={'foo': 'value'})


def test_mount_router_requires():

    async def user_detail():
        return 'result'

    router = Router(requires=(Value('foo'), 'bar'),
                    routes=[Route('/route', user_detail)])

    mortar = Mortar(routes=[Mount('/router', router=router)])
    app = mortar.app()

    with TestClient(app) as client:
        with ShouldRaise(ContextError) as s:
            client.get("/router/route?bar=value")
        compare(s.raised.text, expected="No Value('foo') in context")

        mortar.context.add('value', provides='foo')

        with ShouldRaise(ContextError) as s:
            client.get("/router/route")
        compare(s.raised.text, expected="No FromRequest('bar') in context")

        response = client.get("/router/route?bar=value")
        compare(response.json(), expected='result')


def test_mortar_requires_mount_app():
    async def app(scope, receive, send):
        await PlainTextResponse('some content')(scope, receive, send)

    mortar = Mortar(requires=Value('foo'), routes=[Mount('/app', app=app)])
    app = mortar.app()

    with TestClient(app) as client:

        with ShouldRaise(ContextError):
            client.get("/app")

        mortar.context.add('value', provides='foo')

        compare(client.get("/app").content, expected=b'some content')


def test_mortar_requires_mount_router():

    async def user_detail():
        return 'result'

    router = Router(routes=[Route('/route', user_detail)])

    mortar = Mortar(requires=Value('foo'), routes=[Mount('/router', router=router)])
    app = mortar.app()

    with TestClient(app) as client:
        with ShouldRaise(ContextError):
            client.get("/router/route")

        mortar.context.add('value', provides='foo')

        response = client.get("/router/route")
        compare(response.json(), expected='result')


def test_mount_nested_requires_at_each_level():

    async def user_detail():
        return 'result'

    router = Router(
        requires='bar',
        routes=[Route('/route', user_detail, requires='baz')]
    )

    mortar = Mortar(requires='foo', routes=[Mount('/router', router=router)])
    app = mortar.app()

    with TestClient(app) as client:
        with ShouldRaise(ContextError) as s:
            client.get("/router/route")
        compare(s.raised.text, expected="No FromRequest('foo') in context")

        with ShouldRaise(ContextError) as s:
            client.get("/router/route?foo=1")
        compare(s.raised.text, expected="No FromRequest('bar') in context")

        with ShouldRaise(ContextError) as s:
            client.get("/router/route?foo=1&bar=2")
        compare(s.raised.text, expected="No FromRequest('baz') in context")

        response = client.get("/router/route?foo=1&bar=2&baz=3")
        compare(response.json(), expected='result')


def test_mount_nested_requires_at_each_level_using_requires_type():

    async def user_detail():
        return 'result'

    router = Router(
        requires=requires('bar'),
        routes=[Route('/route', user_detail, requires=requires('baz'))]
    )

    mortar = Mortar(requires=requires('foo'), routes=[Mount('/router', router=router)])
    app = mortar.app()

    with TestClient(app) as client:
        with ShouldRaise(ContextError) as s:
            client.get("/router/route")
        compare(s.raised.text, expected="No Value('foo') in context")

        mortar.context.add('value1', provides='foo')
        with ShouldRaise(ContextError) as s:
            client.get("/router/route")
        compare(s.raised.text, expected="No Value('bar') in context")

        mortar.context.add('value2', provides='bar')
        with ShouldRaise(ContextError) as s:
            client.get("/router/route")
        compare(s.raised.text, expected="No Value('baz') in context")

        mortar.context.add('value3', provides='baz')
        response = client.get("/router/route")
        compare(response.json(), expected='result')


def test_mount_nested_requires_at_each_level_using_both_requires_type_and_strings():

    async def user_detail():
        return 'result'

    router1 = Router(
        requires=requires('baz'),
        routes=[Route('/route', user_detail, requires='bob')]
    )

    router2 = Router(
        requires='bar',
        routes=[Mount('/child', router=router1)]
    )

    mortar = Mortar(
        requires=requires('foo'),
        routes=[Mount('/parent', router=router2)])
    app = mortar.app()

    with TestClient(app) as client:
        with ShouldRaise(ContextError):
            client.get("/parent/child/route")

        mortar.context.add('value1', provides='foo')
        mortar.context.add('value2', provides='baz')
        response = client.get("/parent/child/route?bar=1&bob=2")

        compare(response.json(), expected='result')


def test_requires_requires_type_with_kw():

    mortar = Mortar(
        routes=[Route('/route', context_contents, requires=requires(x='bob'))]
    )
    app = mortar.app()

    with TestClient(app) as client:
        with ShouldRaise(ContextError) as s:
            client.get("/route")
        compare(s.raised.text, expected="No Value('bob') in context")

        mortar.context.add('value', provides='bob')
        response = client.get("/route")

        compare(response.status_code, expected=200)


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
