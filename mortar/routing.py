from functools import partial
from itertools import chain
from typing import Callable, Sequence, List, Dict, Union, Type, Iterable

from mush.asyncio import Context, Runner
from mush.declarations import returns_nothing, requires as mush_requires
from mush.typing import Requires
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route as StarletteRoute, Mount as StarletteMount
from starlette.types import ASGIApp, Scope, Receive, Send

from .resolvers import requirement_modifier, combine_requires


async def _requires(*args):
    return


class RouteHandler:

    def __init__(
            self,
            context: Context,
            endpoint: Callable,
            tweens: Iterable[Callable],
            requires: Requires = None
    ):
        self.context = context
        self.runner = Runner(*tweens, requirement_modifier=requirement_modifier)
        if requires:
            self.runner.add(_requires, requires, returns_nothing)
        self.runner.add(endpoint)

    async def __call__(self, request: Request) -> JSONResponse:
        context = self.context.nest()
        context.add(request, Request)
        return JSONResponse(await self.runner(context))


class Route:

    def __init__(
            self,
            path: str,
            endpoint: Callable,
            *,
            methods: List[str] = None,
            name: str = None,
            tweens: Iterable[Callable] = (),
            requires: Requires = None,
    ):
        self.path: str = path
        self.endpoint: Callable = endpoint
        self.methods: List[str] = methods
        self.name: str = name
        self.tweens: Iterable[Callable] = tweens
        self.requires: Requires = requires

    def starlette_route(
            self,
            context: Context,
            tweens: Iterable[Callable],
            requires: Requires = None
    ):
        # https://github.com/encode/starlette/issues/886 covers why we reference __call__
        # on async callable objects.
        return StarletteRoute(
            self.path,
            RouteHandler(
                context,
                self.endpoint,
                chain(tweens, self.tweens),
                requires=combine_requires(requires, self.requires)
            ).__call__,
            methods=self.methods,
            name=self.name
        )


class MountedAppMiddleware:
    def __init__(
            self,
            context: Context,
            app: ASGIApp,
            tweens: Iterable[Callable] = (),
            requires: Requires = None
    ):
        self.context = context
        self.runner = Runner(*tweens)
        if requires:
            self.runner.add(_requires, requires, returns_nothing)
        self.runner.add(app, mush_requires(Scope, Receive, Send), returns_nothing)

    async def __call__(self, scope, receive, send):
        context = self.context.nest()
        context.add(scope, provides=Scope)
        context.add(receive, provides=Receive)
        context.add(send, provides=Send)
        await self.runner(context)


class Mount:
    def __init__(
        self,
        path: str,
        app: ASGIApp = None,
        router: 'Router' = None,
        name: str = None,
    ):
        self.path = path
        self.app = app
        self.router = router
        self.name = name

    def starlette_route(
            self, context: Context,
            tweens: Iterable[Callable],
            requires: Requires = None
    ):
        if self.router is None:
            routes = None
            app = self.app
            tweens = tuple(tweens)  # unwind any chain passed in
            if app is not None and (tweens or requires):
                app = MountedAppMiddleware(context, app, tweens, requires)
        else:
            routes = self.router.starlette_routes(context, tweens, requires)
            app = None
        return StarletteMount(self.path, app, routes, self.name)


class Router:
    def __init__(
            self,
            routes: List[Union[Route, Mount]],
            tweens: Iterable[Callable] = (),
            requires: Requires = None,
    ):
        self.routes: List[Union[Route, Mount]] = routes
        self.tweens: Iterable[Callable] = tweens
        self.requires: Requires = requires

    def starlette_routes(
            self,
            context: Context,
            tweens: Iterable[Callable] = (),
            requires: Requires = None
    ):
        requires = combine_requires(requires, self.requires)
        return [route.starlette_route(context, chain(tweens, self.tweens), requires)
                for route in self.routes]


class LifecycleMiddleware:
    def __init__(self, app: ASGIApp, context: Context, lifespan: Sequence[Callable]):
        self.app = app
        self.context = context
        self.lifespan = Runner(*lifespan)

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'lifespan':
            lifespan = self.lifespan.clone()
            lifespan.add(partial(self.app, scope, receive, send))
            await lifespan(self.context)
        else:
            await self.app(scope, receive, send)


class Mortar:

    def __init__(
            self,
            lifespan: Sequence[Callable] = (),
            middleware: Sequence[Middleware] = (),
            tweens: Sequence[Callable] = (),
            requires: Requires = None,
            routes: List[Union[Route, Mount]] = None,
            exception_handlers: Dict[Union[int, Type[Exception]], Callable] = None,
            debug: bool = False
    ):
        self.context = Context(requirement_modifier)
        self.middleware = []
        if lifespan:
            self.middleware.append(
                Middleware(LifecycleMiddleware, context=self.context, lifespan=lifespan)
            )
        self.middleware.extend(middleware)
        self.router = Router(routes, tweens, requires)
        self.exception_handlers = exception_handlers
        self.debug = debug

    def app(self):
        return Starlette(
            self.debug,
            self.router.starlette_routes(self.context),
            self.middleware,
            self.exception_handlers
        )
