from functools import cache

from loguru import logger

from app import settings
from app.domain.models import Person
from app.domain.repos import PersonRepository


class SPARQLRepository(PersonRepository):
    def __init__(self, sparql_endpoint: str = settings.SPARQL_ENDPOINT):
        from SPARQLWrapper import DIGEST, JSON, SPARQLWrapper

        self.sparql = SPARQLWrapper(sparql_endpoint)
        self.sparql.setHTTPAuth(DIGEST)
        self.sparql.setCredentials(settings.SPARQL_USERNAME, settings.SPARQL_PASSWORD)
        self.sparql.setReturnFormat(JSON)

    @cache
    def build_prefixes(self):
        return "\n".join(
            f"PREFIX {ns}: <{url}>" for ns, url in settings.NAMESPACES.items()
        )

    def create_person(self, person: Person, **additional_fields):
        import json

        from SPARQLWrapper import POST

        query = self.build_prefixes()
        query += "\n\nINSERT DATA {\n"

        for s, p, o in person.as_triplets():
            query += f'\t{s} {p} "{o}" .\n'

        query += "}"

        logger.debug(f"SPARQL query:\n{query}")

        self.sparql.setMethod(POST)
        self.sparql.setQuery(query)
        response = self.sparql.query().response
        response = json.loads(response.read().decode("utf-8"))
        return response


if __name__ == "__main__":
    repo = SPARQLRepository()
    person_ = Person(uri=":tizio", first_name="Caio", last_name="Sempronio")
    print(repo.create_person(person_))
