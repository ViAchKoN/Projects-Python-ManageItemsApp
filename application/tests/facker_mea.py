import factory
from faker.providers import BaseProvider
from passlib.apps import custom_app_context as pwd_context


class PasswordHashProvider(BaseProvider):
    def password_hash(self) -> str:
        return pwd_context.encrypt('password')


factory.Faker.add_provider(
    PasswordHashProvider,
)


def reg_providers():
    # noop func, to simulate usage in other modules
    ...
