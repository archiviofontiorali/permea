from abc import ABC, abstractmethod
import json
from app.domain.models import Resource


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
