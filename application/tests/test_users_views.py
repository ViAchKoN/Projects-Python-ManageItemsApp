import json

import pytest as pytest
from flask import url_for
from flask_jwt_extended import decode_token

from application.tests.factories.users_factories import UserFactory
from application.users import models


@pytest.fixture
def username() -> str:
    return 'username'


@pytest.fixture
def password() -> str:
    return 'password'


def test_user_registration__ok(
    app_test,
    session,
    username,
    password,
):
    with app_test.test_client() as client:
        response = client.post(
            url_for('users.UserRegistration'),
            data=json.dumps(
                {
                    'username': username,
                    'password': password,
                    'password_confirmation': password,
                }
            ),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        user = models.User.query.filter_by(username=username).first()

        assert response.status_code, 200
        assert user
        assert data == {
            'id': user.id,
            'username': 'username',
        }


def test_user_registration__username_already_exists__error(
    app_test,
    session,
    password,
):
    user = UserFactory.create()

    with app_test.test_client() as client:
        response = client.post(
            url_for('users.UserRegistration'),
            data=json.dumps(
                {
                    'username': user.username,
                    'password': password,
                    'password_confirmation': password,
                }
            ),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 409
        assert data == {
            'message': 'User with this username already exists',
            'status_code': 409,
        }


def test_user_login__ok(
    app_test,
    session,
    password,
):
    user = UserFactory.create()

    with app_test.test_client() as client:
        response = client.post(
            url_for('users.UserLogIn'),
            data=json.dumps(
                {
                    'username': user.username,
                    'password': password,
                }
            ),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 200
        assert 'auth_token' in data

        token_data = decode_token(data['auth_token'])
        assert user.id == token_data['sub']


def test_user_login__user_not_found__error(
    app_test,
    session,
    username,
    password,
):
    with app_test.test_client() as client:
        response = client.post(
            url_for('users.UserLogIn'),
            data=json.dumps(
                {
                    'username': username,
                    'password': password,
                }
            ),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 422
        assert data == {
            'message': 'User not found',
            'status_code': 422,
        }


def test_user_login__user_wrong_credentials__error(
    app_test,
    session,
):
    user = UserFactory.create()

    with app_test.test_client() as client:
        response = client.post(
            url_for('users.UserLogIn'),
            data=json.dumps(
                {
                    'username': user.username,
                    'password': 'invalid_password',
                }
            ),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 401
        assert data == {
            'message': 'Wrong credentials provided',
            'status_code': 401,
        }
