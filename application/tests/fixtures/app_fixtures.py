import pytest

from application import create_app
from application.config import CONFIG


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture(scope='session')
def app_test():
    app = create_app()
    app.config.from_object('application.config.TestingConfig')
    return app


@pytest.fixture
def config_yaml():
    return CONFIG
