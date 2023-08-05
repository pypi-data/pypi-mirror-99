# Define the application directory
import os
import logging
from emannotationschemas.models import Base
from flask_sqlalchemy import SQLAlchemy
import json


class BaseConfig:
    ENV = "base"
    HOME = os.path.expanduser("~")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    TESTING = False
    LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    LOGGING_LOCATION = HOME + "/.materializationengine/bookshelf.log"
    LOGGING_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = "redis://"
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    LOCAL_SERVICE_URL = os.environ.get("LOCAL_SERVICE_URL")
    ANNO_ENDPOINT = f"https://{LOCAL_SERVICE_URL}/annotation/"
    INFOSERVICE_ENDPOINT = "https://global.daf-apis.com/info"
    AUTH_URI = "https://global.daf-apis.com/auth"
    GLOBAL_SERVER = "https://global.daf-apis.com"
    SCHEMA_SERVICE_ENDPOINT = "https://global.daf-apis.com/schema/"
    SEGMENTATION_ENDPOINT = "https://global.daf-apis.com/"
    MASTER_NAME = os.environ.get("MASTER_NAME", None)
    MATERIALIZATION_ROW_CHUNK_SIZE = 500
    QUERY_LIMIT_SIZE = 200000
    CELERY_WORKER_IP = os.environ.get("CELERY_WORKER_IP", "127.0.0.1")
    DATASTACKS = ["minnie65_phase3_v1"]
    DAYS_TO_EXPIRE = 7
    LTS_DAYS_TO_EXPIRE = 30
    INFO_API_VERSION = 2
    AUTH_DATABASE_NAME = "minnie65"
    if os.environ.get("DAF_CREDENTIALS", None) is not None:
        with open(os.environ.get("DAF_CREDENTIALS"), "r") as f:
            AUTH_TOKEN = json.load(f)["token"]
    else:
        AUTH_TOKEN = ""


class DevConfig(BaseConfig):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:materialize@db:5432/materialize"
    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PORT = os.environ.get("REDIS_PORT")
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
    USE_SENTINEL = os.environ.get("USE_SENTINEL", False)

class TestConfig(BaseConfig):
    ENV = "testing"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = "memory://"
    CELERY_RESULT_BACKEND = "redis://"


class ProductionConfig(BaseConfig):
    ENV = "production"
    LOGGING_LEVEL = logging.INFO
    CELERY_BROKER = os.environ.get("REDIS_URL")
    CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL")
    REDIS_URL = os.environ.get("REDIS_URL")


config = {
    "default": "materializationengine.config.BaseConfig",
    "development": "materializationengine.config.DevConfig",
    "testing": "materializationengine.config.TestConfig",
    "production": "materializationengine.config.ProductionConfig",
}


def configure_app(app):
    config_name = os.getenv("FLASK_CONFIGURATION", "default")
    # object-based default configuration
    app.config.from_object(config[config_name])
    if "MATERIALIZATION_ENGINE_SETTINGS" in os.environ.keys():
        app.config.from_envvar("MATERIALIZATION_ENGINE_SETTINGS")
    # instance-folders configuration
    app.config.from_pyfile("config.cfg", silent=True)
    app.logger.debug(app.config)
    db = SQLAlchemy(model_class=Base)
    db.init_app(app)
    app.app_context().push()
    return app
