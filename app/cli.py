from typing import Literal

from rdflib import Graph, URIRef
from typer import Typer, echo

from . import settings

cli = Typer()


@cli.command()
def hello():
    echo(f"Hello, World!")


def initialize_graph(
    endpoint: str = settings.SPARQL_ENDPOINT,
    identifier: str = settings.SPARQL_DEFAULT_IDENTIFIER,
    mode: Literal["store", "update", "query"] = "query",
):
    opts = dict(identifier=identifier)
    match mode:
        case "query":
            graph = Graph(store="SPARQLStore", **opts)
        case "update":
            graph = Graph(store="SPARQLUpdateStore", **opts)
        case _:
            raise NotImplementedError

    graph.open(f"{endpoint}/{mode}")

    return graph


@cli.command()
def read_data(identifier: str = settings.SPARQL_DEFAULT_IDENTIFIER):
    graph = initialize_graph(mode="query", identifier=identifier)

    for s, p, o in graph.query(r"SELECT * WHERE { ?sub ?pred ?obj . } LIMIT 3"):
        echo(f"{s} | {p} | {o}")


@cli.command()
def load_data(identifier: str = settings.SPARQL_DEFAULT_IDENTIFIER):
    graph = initialize_graph(mode="update", identifier=identifier)

    query = """
        PREFIX :<http://bedrock/>
        INSERT DATA {
            :fred :hasSpouse :wilma .
            :fred :hasChild :pebbles .
            :wilma :hasChild :pebbles .
            :pebbles :hasSpouse :bamm-bamm ; :hasChild :roxy, :chip. 
        }
    """
    graph.update(query)

    graph.close()


if __name__ == "__main__":
    cli()
