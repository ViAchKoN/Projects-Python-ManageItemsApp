import typing as tp

import pytest

from application.tests.factories.users_factories import UserFactory
from application.users import models


@pytest.fixture
def auth_login(session):
    def create_auth_token(user: models.User = None) -> tp.Tuple[models.User, str]:
        if user is None:
            user = UserFactory.create()
        auth_token = user.encode_auth_token()
        return user, auth_token

    return create_auth_token
