import datetime
import typing as tp

import pytest
from flask_jwt_extended import create_access_token

from application.items import models as items_models
from application.tests.factories.items_factories import ItemFactory
from application.tests.factories.users_factories import UserFactory
from application.users import models


@pytest.fixture
def send_item_token(session):
    def create_send_item_token(
        user: models.User,
        item: items_models.Item = None,
    ) -> tp.Tuple[items_models.Item, str]:
        if item is not None and user == item.user:
            raise ValueError(
                'The owner of the item cant be the same as the user passed in the function.'
            )
        elif item is None:
            item = ItemFactory.create(user=UserFactory.create())

        return item, create_access_token(
            user.id,
            additional_claims={'item_id': item.id},
            expires_delta=datetime.timedelta(hours=2),
        )

    return create_send_item_token
