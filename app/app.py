import random

from pydantic import BaseModel
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.templating import Jinja2Templates

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


async def search(request):
    context = {"rows": db}
    return templates.TemplateResponse(request, "partials/search.html", context)


async def create_node(request):
    context = {
        "lod": db[request.path_params["id"]],
        "top": random.randint(0, 10) * 20,
        "left": random.randint(0, 10) * 20,
    }
    return templates.TemplateResponse(request, "partials/card.html", context)


routes = [
    Route("/", endpoint=homepage),
    Route("/search", endpoint=search),
    Route("/node/{id:int}", endpoint=create_node, methods=["POST"]),
]

app = Starlette(debug=True, routes=routes)
