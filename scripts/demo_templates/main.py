from pathlib import Path

from jinja2 import Environment
from pydantic import BaseModel
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route, request_response
from starlette.templating import Jinja2Templates

jinja = Environment()


class Jinja2Renderer:
    def __init__(self, template_directory: Path):
        self.templates = Jinja2Templates(directory=template_directory)

    def render(self, request, template_name: str, context: dict = None):
        context = context or {}
        return self.templates.TemplateResponse(request, template_name, context=context)


class PageTemplate(BaseModel):
    query: str
    view: str


class BaseView:
    def __call__(self, request):
        return HTMLResponse("Hello world!")


class ExampleView:
    def __init__(self, renderer: Jinja2Renderer):
        self.renderer = renderer

    async def __call__(self, request):
        page = PageTemplate(query="", view="<b>title</b>: {{ title }}")

        if request.method == "POST":
            form = await request.form()
            page.view = form.get("template")

        context = {"title": "Hi", "template": page.view}
        main = jinja.from_string(page.view).render(context)
        context.setdefault("main", main)
        return self.renderer.render(request, "index.html", context=context)


renderer = Jinja2Renderer(Path(__file__).parent)

app = Starlette(debug=True)
app.add_route("/", ExampleView(renderer).__call__, methods=["GET", "POST"])
