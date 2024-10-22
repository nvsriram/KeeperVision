from os import getenv

from dotenv import load_dotenv
from flask import Flask

load_dotenv()

application = Flask(__name__)


def get_database_uri():
    # ensure .env is setup properly
    username = getenv("DATABASE_USERNAME")
    if not username:
        raise RuntimeError(f"DATABASE_USERNAME is not set")
    password = getenv("DATABASE_PASSWORD")
    if not password:
        raise RuntimeError(f"DATABASE_PASSWORD is not set")
    host = getenv("DATABASE_HOST")
    if not host:
        raise RuntimeError(f"DATABASE_HOST is not set")
    dbname = getenv("DATABASE_NAME")
    if not dbname:
        raise RuntimeError(f"DATABASE_NAME is not set")

    return f"mysql+pymysql://{username}:{password}@{host}/{dbname}?charset=utf8mb4"


application.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
