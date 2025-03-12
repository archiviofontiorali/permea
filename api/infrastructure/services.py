import json
from abc import ABC, abstractmethod
from typing import Literal

from loguru import logger

from app import settings
from pydantic import BaseModel, HttpUrl


class LinkedData(BaseModel):
    type: Literal["uri"]
    value: HttpUrl


SPARQLSelectRow = dict[str, LinkedData]


class SPARQLService(ABC):
    @abstractmethod
    def select(self, query: str) -> list[SPARQLSelectRow]:
        pass

    @abstractmethod
    def insert(self, query: str):
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

    def select(self, query: str) -> list[SPARQLSelectRow]:
        logger.debug(f"Select query:\n{query}")
        content = self._execute_query(query)
        return [
            {key: LinkedData.model_validate(value)}
            for row in content["results"]["bindings"]
            for key, value in row.items()
        ]

    def insert(self, query: str):
        logger.debug(f"Update query:\n{query}")
        response = self._execute_query(query, method="POST")
        assert response["statusCode"] == 200
