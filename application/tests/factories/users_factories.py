import random

import factory

from application.tests import faker_mea
from application.tests.factories.utils import SQLAlchemyModelFactory
from application.users import models

faker_mea.reg_providers()


class UserFactory(SQLAlchemyModelFactory):
    username = factory.Faker('user_name')
    password_hash = factory.Faker('password_hash')

    class Meta:
        model = models.User

    class Params:
        items = factory.Trait(
            _items=factory.RelatedFactoryList(
                'application.tests.factories.items_factories.ItemFactory',
                factory_related_name='user',
                size=random.randrange(1, 10),
            )
        )
