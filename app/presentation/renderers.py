import json
from abc import ABC, abstractmethod

from app.domain.models import Resource, TemplateForm, TemplateView


class ResourceRenderer(ABC):
    @abstractmethod
    def render(self, resource: Resource) -> str:
        pass


class PlainResourceRenderer(ResourceRenderer):
    def render(self, resource):
        return "\n".join(f"{k}: {v}" for k, v in resource)


class JSONResourceRenderer(ResourceRenderer):
    def render(self, resource: Resource) -> str:
        return json.dumps(resource.model_dump())


class Jinja2Renderer:
    def render(self, template_name: str, **data) -> str:
        raise NotImplementedError()
