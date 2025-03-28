from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import settings

templates = Jinja2Templates(directory="templates")


async def homepage(request):
    return templates.TemplateResponse(request, "index.html")


class Card:
    async def get_card(self, request):
        return templates.TemplateResponse(request, "partials/card.html")


routes = [
    Route("/", endpoint=homepage),
    Route("/add-card", endpoint=Card().get_card, methods=["POST"]),
    Mount("/", StaticFiles(directory=settings.STATIC_FOLDER), name="static"),
]

app = Starlette(debug=True, routes=routes)
