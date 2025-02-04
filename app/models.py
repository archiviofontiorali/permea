from typing import Union

from pydantic import BaseModel, HttpUrl

Identifier = Union[HttpUrl, str]


class Triplet(BaseModel):
    subject: str
    predicate: str
    object: str


class Resource(BaseModel):
    id: Identifier
    type: HttpUrl | str

    # triples: list[Triplet]
