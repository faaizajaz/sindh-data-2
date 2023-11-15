import os

from dotenv import load_dotenv

cwd = os.getcwd()
dotenv_path = os.path.join(cwd, os.getenv("ENVIRONMENT_FILE", ".env.dev"))
load_dotenv(dotenv_path=dotenv_path, override=True)

APP_HOST = os.environ.get("HOST")
APP_PORT = os.environ.get("PORT")
APP_DEBUG = bool(os.environ.get("DEBUG"))
MAPBOX_TOKEN = os.environ.get("MAPBOX_TOKEN", None)
