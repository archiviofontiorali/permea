from pathlib import Path

from decouple import config

PROJECT_FOLDER = Path(__file__).parent.parent
HIDDEN_DATA_FOLDER = PROJECT_FOLDER / ".data"

SPARQL_ENDPOINT = config("SPARQL_ENDPOINT", "http://localhost:7878")
