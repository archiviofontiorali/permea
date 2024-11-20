from pathlib import Path

from decouple import config

PROJECT_FOLDER = Path(__file__).parent.parent
HIDDEN_DATA_FOLDER = PROJECT_FOLDER / ".data"

BERKELEY_DB_PATH = config("BERKELEY_DB_PATH", HIDDEN_DATA_FOLDER / "berkeley.db", Path)
