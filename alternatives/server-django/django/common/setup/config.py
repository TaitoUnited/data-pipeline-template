import os
from collections import defaultdict


def read_secret(name: str) -> str:
    if _config[name]:
        return _config[name]
    try:
        with open(f"/run/secrets/{name}", "r") as secret:
            return secret.read()
    except FileNotFoundError:
        print("WARNING: Secret file /run/secrets/" + name + " not found")
        return ""


_config = defaultdict(
    lambda: None,  # type: ignore
    os.environ,
)


class Config:
    ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

    # Labeling
    COMMON_PROJECT = _config["COMMON_PROJECT"]
    COMMON_COMPANY = _config["COMMON_COMPANY"]
    COMMON_FAMILY = _config["COMMON_FAMILY"]
    COMMON_APPLICATION = _config["COMMON_APPLICATION"]
    COMMON_SUFFIX = _config["COMMON_SUFFIX"]
    COMMON_IMAGE_TAG = _config["COMMON_IMAGE_TAG"]
    APP_NAME = "data-pipeline-template-server"
    APP_VERSION = (
        f"{_config['BUILD_VERSION']}+local"
        if not _config["BUILD_IMAGE_TAG"]
        else f"{_config['BUILD_VERSION']}+{_config['BUILD_IMAGE_TAG']}"
    )

    # Environment
    COMMON_ENV = _config["COMMON_ENV"]  # dev / test / stag / prod
    PYTHON_ENV = _config["PYTHON_ENV"]  # development / production
    COMMON_DOMAIN = _config["COMMON_DOMAIN"]  # myapp.mydomain.com

    # API
    API_PORT = int(_config.get("API_PORT", -1))
    API_BINDADDR = _config["API_BINDADDR"]
    API_KEY = read_secret("API_KEY")
    API_KEY_ETL = read_secret("API_KEY_ETL")

    CORS_ORIGINS = (
        [x.strip() for x in _config["CORS_ORIGINS"].split(",")]
        if _config["CORS_ORIGINS"]
        else []
    )

    # Database
    DATABASE_HOST = _config["DATABASE_HOST"]
    DATABASE_PORT = int(_config.get("DATABASE_PORT", 5432))
    DATABASE_NAME = _config["DATABASE_NAME"]
    DATABASE_USER = _config["DATABASE_USER"]
    DATABASE_PASSWORD = read_secret("DATABASE_PASSWORD")
    DATABASE_POOL_MAX = int(_config.get("DATABASE_POOL_MAX", 10))
    DATABASE_POOL_MIN = int(_config.get("DATABASE_POOL_MIN", 1))
    DATABASE_MAX_RETRIES = int(_config.get("DATABASE_MAX_RETRIES", 5))

    # Storage
    STORAGE_TYPE = _config["STORAGE_TYPE"]
    STORAGE_ENDPOINT = _config["STORAGE_ENDPOINT"]
    STORAGE_ACCESS_KEY = _config["STORAGE_ACCESS_KEY"]
    STORAGE_SECRET_KEY = read_secret("STORAGE_SECRET_KEY")
    STORAGE_BUCKET = _config["STORAGE_BUCKET"]

    # Logging
    COMMON_LOG_LEVEL = _config["COMMON_LOG_LEVEL"]
    COMMON_LOG_FORMAT = _config["COMMON_LOG_FORMAT"]
    DEBUG = _config["COMMON_DEBUG"] == "true"

    # Testing
    TESTING = False
