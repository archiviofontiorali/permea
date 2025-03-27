from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from . import settings

templates = Jinja2Templates(directory="templates")


async def homepage(request):
    return templates.TemplateResponse(request, "index.html")


routes = [
    Route("/", endpoint=homepage),
    Mount("/", StaticFiles(directory=settings.STATIC_FOLDER), name="static"),
]

app = Starlette(debug=True, routes=routes)
