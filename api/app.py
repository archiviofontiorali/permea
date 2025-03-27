"""Define the main application"""

from typer import Typer

from app.application.cases import PersonCase
from app.infrastructure.repositories import MockRepository
from app.presentation.handlers import PersonRoute
from app.presentation.renderers import (
    JSONResourceRenderer,
    PlainResourceRenderer,
    ResourceRenderer,
)


class Container[T]:
    def __init__(self, **kwargs: T):
        self.__dict__.update(kwargs)

    def __getattr__(self, item: str) -> T:
        return self.__dict__[item]


class App:
    def __init__(self):
        self.services = Container()
        r = self.repos = Container(person=MockRepository())
        c = self.cases = Container(person=PersonCase(repo=r.person))

        e = self.renderers = Container[ResourceRenderer](
            plain=PlainResourceRenderer(),
            json=JSONResourceRenderer(),
        )

        self.handlers = Container(
            person=PersonRoute(c.person, base_renderer=e.plain, json_renderer=e.json)
        )

    def build_cli(self):
        cli = Typer()
        h = self.handlers

        cli.command("person")(h.person.__call__)

        return cli
