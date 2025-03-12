from typing import Annotated

from pydantic import BaseModel, ConfigDict
from rdflib import URIRef as URI
from rdflib.namespace import FOAF, RDF

from app import settings

ResourceID = str
URIType = Annotated[URI, RDF.type]


class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Resource(Model):
    id: ResourceID
    type: URIType

    @property
    def uri(self):
        return settings.NAMESPACE[self.id]


class Person(Resource):
    type: URIType = FOAF.Person
    first_name: Annotated[str, FOAF.firstName]
    last_name: Annotated[str, FOAF.lastName]


class TemplateView(Model):
    query: str  # A SPARQL SELECT query to retrieve fields
    view: str  # A vue.js template to render qith query data


class TemplateForm(Model):
    query: str  # A SPARQL INSERT query for sending data
    form: str  # A vue.js template with a form
