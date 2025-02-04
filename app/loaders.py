import abc

from loguru import logger
from rdflib import Graph, URIRef

from .models import Identifier, Resource

PREFIX = {
    "ex": "<http://example.org/>",
    "rdf": "<http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
    "foaf": "<http://xmlns.com/foaf/0.1/>",
}


class TripletStore(abc.ABC):
    def fetch_resource(self, identifier: Identifier):
        raise NotImplementedError()

    def load_resource(self, resource: Resource):
        raise NotImplementedError()


class SPARQLTripletStore(TripletStore):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.graph = Graph()

        self.graph.parse(f"http://{host}:{port}/prova")
        self.prefix = "\n".join(f"PREFIX {k}:{v}" for k, v in PREFIX.items())

    def fetch_resource(self, identifier: Identifier):
        query = f"""
            {self.prefix}

            SELECT ?s ?v ?p
            WHERE {{
                ?s ?v ?p .
                ?s rdf:type foaf:Person .
            }}
        """
        logger.debug(query)

        return self.graph.query(query)

    def load_resource(self, resource: Resource):
        query = f"""
            {self.prefix}

            INSERT DATA {{
                {resource.id} rdf:type {resource.type}
            }}
        """
        logger.debug(query)
        # TODO: https://github.com/RDFLib/sparqlwrapper is needed
        return self.graph.update(query)


if __name__ == "__main__":
    store = SPARQLTripletStore("localhost", 3030)

    person = Resource(
        id=f"ex:me2",
        type=f"foaf:Person",
    )
    response = store.load_resource(person)
    print(response)

    response = store.fetch_resource("")
    for r in response:
        print(r)
