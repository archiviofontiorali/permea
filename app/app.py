import random
import uuid

from pydantic import BaseModel

from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import settings

templates = Jinja2Templates(directory="templates")


class LinkedOpenData(BaseModel):
    id: int
    title: str
    description: str


db = [
    LinkedOpenData(id=0, title="title_a", description=""),
    LinkedOpenData(id=1, title="title_b", description=""),
    LinkedOpenData(id=2, title="title_c", description=""),
]


async def homepage(request):
    return templates.TemplateResponse(request, "index.html")


class Card:
    async def create_edge(self, request):
        context = {}
        return templates.TemplateResponse(request, "partials/edge.html", context)

    async def get_row(self, request):
        context = {"id": uuid.uuid4()}
        return templates.TemplateResponse(request, "partials/row.html", context)

    async def get_card(self, request):
        context = {
            "id": uuid.uuid4(),
            "top": random.randint(0, 30),
            "left": random.randint(0, 30),
        }
        return templates.TemplateResponse(request, "partials/card.html", context)


routes = [
    Route("/", endpoint=homepage),
    Route("/add-row", endpoint=Card().get_row, methods=["POST"]),
    Route("/add-card", endpoint=Card().get_card, methods=["POST"]),
    Route("/edge", endpoint=Card().create_edge, methods=["POST"]),
    Mount("/", StaticFiles(directory=settings.STATIC_FOLDER), name="static"),
]

app = Starlette(debug=True, routes=routes)
