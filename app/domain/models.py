from typing import Annotated

from pydantic import BaseModel
from app import settings

from rdflib import URIRef as URI
from rdflib.namespace import FOAF, RDF

from pydantic import ConfigDict

ResourceID = str
URIType = Annotated[URI, RDF.type]


class Resource(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ResourceID
    type: URIType

    @property
    def uri(self):
        return settings.NAMESPACE[self.id]


class Person(Resource):
    type: URIType = FOAF.Person
    first_name: Annotated[str, FOAF.firstName]
    last_name: Annotated[str, FOAF.lastName]
