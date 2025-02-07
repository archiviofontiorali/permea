from pathlib import Path

from decouple import config

PROJECT_FOLDER = Path(__file__).parent.parent
HIDDEN_DATA_FOLDER = PROJECT_FOLDER / ".data"

SPARQL_ENDPOINT = config("SPARQL_ENDPOINT", "http://localhost:7878")
SPARQL_USERNAME = config("SPARQL_USERNAME", "admin")
SPARQL_PASSWORD = config("SPARQL_PASSWORD", "changeme")

SPARQL_DEFAULT_IDENTIFIER = config("SPARQL_DEFAULT_IDENTIFIER", "default")


BASE_URL = "http://localhost/"

NAMESPACES = {
    "": BASE_URL,
    "ex": "http://example.org/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "foaf": "http://xmlns.com/foaf/0.1/",
}
