import factory

from application.items import models
from application.tests import faker_mea
from application.tests.factories.users_factories import UserFactory
from application.tests.factories.utils import SQLAlchemyModelFactory

faker_mea.reg_providers()


class ItemFactory(SQLAlchemyModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Faker('word')

    class Meta:
        model = models.Item
