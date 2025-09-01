from pathlib import Path

from environs import env, validate

env.read_env()


PROJECT_FOLDER = Path(__file__).parent.parent
APP_FOLDER = PROJECT_FOLDER / "app"
STATIC_FOLDER = PROJECT_FOLDER / "www" / "static"

BASE_URL = env.str("BASE_URL", default=":::", validate=validate.URL())
