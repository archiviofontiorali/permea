from dataclasses import dataclass
from typing import Annotated

from loguru import logger
from pydantic import BaseModel

URI = str


class Model(BaseModel):
    pass


class Resource(Model):
    uri: URI

    def get_property_uri(self, field_name: str) -> URI:
        try:
            return self.model_fields.get(field_name).metadata[0].uri
        except IndexError:
            logger.debug(self.model_fields.get(field_name))
            raise Exception(f"Missing annotation in field {field_name}")

    def as_triplets(self):
        return [
            (self.uri, self.get_property_uri(field), getattr(self, field))
            for field, value in self
            if field not in {"uri"}
        ]


@dataclass
class Property:
    uri: URI


class Person(Resource):
    first_name: Annotated[str, Property(uri="foaf:firstName")]
    last_name: Annotated[str, Property(uri="foaf:lastName")]


# NAMESPACE_RE = re.compile(r"^(?P<ns>\w+):(?P<reference>.*)")
#
#
# def expand_prefix(value: HttpUrl | str) -> HttpUrl | str:
#     if not isinstance(value, str) or (match := NAMESPACE_RE.match(value)) is None:
#         return value
#
#     if (namespace := match.group("ns")) in {"http", "https"}:
#         return value
#
#     if (prefix := settings.NAMESPACES.get(namespace)) is None:
#         raise ValueError(f"Unsupported namespace '{namespace}'")
#
#     return f"{prefix}{match.group('reference')}"
#
