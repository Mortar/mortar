from functools import partial
from typing import Callable, Sequence, List, Dict, Union, Type

from mush.asyncio import Context, Runner
from mush.declarations import returns_nothing
from mush.typing import Requires
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route as StarletteRoute

from .resolvers import requirement_modifier


class Route:

    def __init__(
            self,
            path: str,
            endpoint: Callable,
            *,
            methods: List[str] = None,
            name: str = None,
            tweens: Sequence[Callable] = (),
            requires: Requires = None,
    ):
        self.path: str = path
        self.endpoint: Callable = endpoint
        self.methods: List[str] = methods
        self.name: str = name
        self.tweens: List[Callable] = list(tweens)
        self.requires: Requires = requires


class RouteHandler:

    def __init__(self,
                 context: Context,
                 endpoint: Callable,
                 *tweens: Sequence[Callable],
                 requires: Requires = None):
        self.context = context
        self.runner = Runner(*tweens, requirement_modifier=requirement_modifier)
        if requires:
            self.runner.add(lambda *args: None, requires, returns_nothing)
        self.runner.add(endpoint)

    async def __call__(self, request: Request) -> JSONResponse:
        context = self.context.nest()
        context.add(request, Request)
        return JSONResponse(await self.runner(context))


class LifecycleMiddleware:
    def __init__(self, app, lifespan):
        self.app = app
        self.lifespan = Runner(*lifespan)

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'lifespan':
            lifespan = self.lifespan.clone()
            lifespan.add(partial(self.app, scope, receive, send))
            await lifespan()
        else:
            await self.app(scope, receive, send)


class Mortar:

    def __init__(self,
                 lifespan: Sequence[Callable] = (),
                 middleware: Sequence[Middleware] = (),
                 tweens: Sequence[Callable] = (),
                 routes: Sequence[Route] = None,
                 exception_handlers: Dict[Union[int, Type[Exception]], Callable] = None,
                 debug: bool = False):
        self.context = Context(requirement_modifier)
        self.middleware = []
        if lifespan:
            self.middleware.append(Middleware(LifecycleMiddleware, lifespan=lifespan))
        self.middleware.extend(middleware)
        self.tweens = tweens
        self.routes = routes
        self.exception_handlers = exception_handlers
        self.debug = debug

    def app(self):
        # https://github.com/encode/starlette/issues/886 covers why we reference __call__
        # on async callable objects.

        starlette_routes = []

        for route in self.routes:

            starlette_routes.append(StarletteRoute(
                route.path,
                RouteHandler(
                    self.context,
                    route.endpoint,
                    *self.tweens, *route.tweens,
                    requires=route.requires
                ).__call__,
                methods=route.methods,
                name=route.name
            ))

        app = Starlette(self.debug, starlette_routes, self.middleware, self.exception_handlers)

        return app
