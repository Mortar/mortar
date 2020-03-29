from typing import Callable, Sequence, List

from mush.asyncio import Context
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import BaseRoute, Route as StarletteRoute

from .resolvers import requirement_modifier


class Mortar:

    def __init__(self):
        self.context: Context = Context(requirement_modifier)

    async def run(self, endpoint: Callable, request: Request) -> JSONResponse:
        context = self.context.nest()
        context.add(request, Request)
        return JSONResponse(await context.call(endpoint))


def mortar(*routes: Sequence[BaseRoute], debug: bool = False):
    app = Starlette(debug, routes or None)
    app.state.mortar = Mortar()
    return app


def route(path: str, endpoint: Callable, *, methods: List[str] = None, name: str = None):

    async def run(request: Request):
        return await request.app.state.mortar.run(endpoint, request)

    return StarletteRoute(path, run, methods=methods, name=name)
