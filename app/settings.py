from pathlib import Path

from environs import env, validate

env.read_env()

check_url = dict(validate=validate.URL())


PROJECT_FOLDER = Path(__file__).parent.parent
HIDDEN_DATA_FOLDER = PROJECT_FOLDER / ".data"


BASE_URL = env.str("BASE_URL", default=":::", validate=validate.URL())

with env.prefixed("SPARQL_"):
    SPARQL_ENDPOINT = env.str("ENDPOINT", default="http://localhost:7878", **check_url)
    SPARQL_USERNAME = env.str("USERNAME", default="admin")
    SPARQL_PASSWORD = env.str("PASSWORD", default="changeme")


NAMESPACES = {
    "": BASE_URL,
    "ex": "http://example.org/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "foaf": "http://xmlns.com/foaf/0.1/",
}
