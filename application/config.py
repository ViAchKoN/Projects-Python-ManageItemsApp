import os
import sys

import yaml

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir)
sys.path.append(os.path.dirname(basedir))

CONFIG_PATH = os.path.join(basedir, 'config.yaml')
DB_ADDRESS = 'postgresql://{user}:{password}@{host}:{port}/{database}'


def get_config(path):
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


CONFIG = get_config(CONFIG_PATH)


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = b'&6\x0fm\xb7\xf96\x92s~\xe6G\xa9uj\xee'
    JWT_AUTH_USERNAME_KEY = 'user_id'
    SQLALCHEMY_DATABASE_URI = DB_ADDRESS.format(**CONFIG['postgres'])
    API_TITLE = 'Manage Items App'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_JSON_PATH = 'api-spec.json'
    OPENAPI_SWAGGER_UI_PATH = '/'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SERVER_NAME = 'localhost:105'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = DB_ADDRESS.format(**CONFIG['postgres_test'])
