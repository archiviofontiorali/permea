from functools import cache

from app import settings
from app.domain.models import Person, ResourceID
from app.domain.repos import PersonRepository
from app.infrastructure.services import SPARQLService


class MockRepository(PersonRepository):
    def __init__(self):
        _data = [
            Person(id="tizio-caio", first_name="Tizio", last_name="Caio"),
            Person(id="dr-who", first_name="John", last_name="Smith"),
        ]
        self.data = {value.id: value for value in _data}

    def create_person(self, person):
        if person.uri in self.data:
            raise Exception("Person already exists")
        self.data[person.uri] = person

    def retrieve_person(self, person_id) -> Person:
        return self.data[person_id]


class SPARQLRepository(PersonRepository):
    def __init__(self, service: SPARQLService):
        self.service = service

    @cache
    def _build_prefixes(self):
        return "\n".join(
            f"PREFIX {ns}: <{url}>" for ns, url in settings.NAMESPACES.items()
        )

    def create_person(self, person: Person):
        query = f"""
        {self._build_prefixes()}
        INSERT DATA {{
            {person.uri} foaf:firstName "{person.first_name}" ;
                         foaf:lastName "{person.last_name}" .
        }}
        """
        self.service.insert(query)

    def retrieve_person(self, resource_id) -> Person:
        # query = ...
        # self.service.select(query)
        raise NotImplementedError
