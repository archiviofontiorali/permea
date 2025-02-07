import json
from abc import ABC, abstractmethod
from typing import Literal

from loguru import logger
from pydantic import BaseModel

from app import settings
from app.domain.models import Person


class LinkedData(BaseModel):
    type: Literal["uri", "literal"]
    value: str


SPARQLSelectResponseRow = dict[str, LinkedData]


class SPARQLService(ABC):
    @abstractmethod
    def update(self, query: str):
        pass

    @abstractmethod
    def select(self, query: str):
        pass


class SPARQLWrapperService(SPARQLService):
    def __init__(
        self,
        endpoint: str = settings.SPARQL_ENDPOINT,
        username: str = settings.SPARQL_USERNAME,
        password: str = settings.SPARQL_PASSWORD,
    ):
        from SPARQLWrapper import DIGEST, JSON, SPARQLWrapper

        self.engine = SPARQLWrapper(endpoint)
        self.engine.setHTTPAuth(DIGEST)
        self.engine.setCredentials(username, password)
        self.engine.setReturnFormat(JSON)

    def _execute_query(
        self, query: str, method: Literal["GET", "POST"] = "GET"
    ) -> dict:
        self.engine.setMethod(method)
        self.engine.setQuery(query)

        response = self.engine.query().response
        content = response.read().decode("utf-8")
        content = json.loads(content)

        logger.debug(f"Status code: {response.status}")
        logger.debug(f"Response content:\n{json.dumps(content, indent=2)}")

        return content

    def select(self, query: str) -> list[SPARQLSelectResponseRow]:
        logger.debug(f"Select query:\n{query}")
        content = self._execute_query(query)
        return [
            {key: LinkedData.model_validate(value)}
            for row in content["results"]["bindings"]
            for key, value in row.items()
        ]

    def update(self, query: str):
        logger.debug(f"Update query:\n{query}")
        response = self._execute_query(query, method="POST")
        assert response["statusCode"] == 200


if __name__ == "__main__":
    service = SPARQLWrapperService()

    data = service.select(
        """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT *
        WHERE {
            ?s ?p ?o .
        }
        """
    )

    person = Person(uri=":tizio_caio", first_name="Tizio", last_name="Caio")
    service.update(
        f"""
        PREFIX : <http://localhost/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        INSERT DATA {{
            {person.uri} foaf:firstName "{person.first_name}" ;
                         foaf:lastName "{person.last_name}" .
        }}
        """
    )
