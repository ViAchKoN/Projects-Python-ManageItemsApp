import json
import random

import pytest
from flask import url_for
from flask_jwt_extended import decode_token

from application.items import models
from application.items import schemas
from application.tests.factories.items_factories import ItemFactory
from application.tests.factories.users_factories import UserFactory


@pytest.fixture
def item_name() -> str:
    return 'item_name'


def test_items_new__ok(
    app_test,
    auth_login,
    item_name,
):
    user, auth_token = auth_login()
    with app_test.test_client() as client:
        response = client.post(
            url_for('items.ItemAdd'),
            data=json.dumps(
                {
                    'name': item_name,
                }
            ),
            content_type='application/json',
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
        data = json.loads(response.data.decode())
        item = models.Item.query.filter_by(name=item_name, user=user).first()

        assert response.status_code, 200
        assert item
        assert data == {
            'id': item.id,
            'name': item_name,
            'user_id': user.id,
        }


def test_items_list_get__ok(
    app_test,
    auth_login,
):
    user, auth_token = auth_login()
    ItemFactory.create_batch(user=user, size=4)

    with app_test.test_client() as client:
        response = client.get(
            url_for('items.ItemListGet'),
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
        data = json.loads(response.data.decode())
        assert response.status_code, 200

        items = models.Item.query.filter_by(user=user).all()
        assert len(items), 4
        assert data, schemas.ItemSchema().dumps(many=True)


def test_items_list_get__user_not_found__error(app_test, session):
    user = UserFactory.build()
    auth_token = user.encode_auth_token()
    with app_test.test_client() as client:
        response = client.get(
            url_for('items.ItemListGet'),
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 422
        assert data == {
            'message': 'User not found',
            'status_code': 422,
        }


def test_items_delete__ok(
    app_test,
    auth_login,
):
    user, auth_token = auth_login()
    item_id = random.choice(ItemFactory.create_batch(user=user, size=4)).id
    with app_test.test_client() as client:
        response = client.delete(
            url_for('items.ItemDelete', item_id=item_id),
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 200
        assert models.Item.query.filter_by(id=item_id), None

        assert data == {
            'message': 'ok',
            'status_code': 200,
        }


def test_items_delete__user_not_found__error(app_test, session):
    user = UserFactory.build()
    auth_token = user.encode_auth_token()
    with app_test.test_client() as client:
        response = client.delete(
            url_for('items.ItemDelete', item_id=1),
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 422
        assert data == {
            'message': 'User not found',
            'status_code': 422,
        }


def test_items_delete__item_not_found__error(app_test, auth_login):
    user, auth_token = auth_login()
    with app_test.test_client() as client:
        response = client.delete(
            url_for('items.ItemDelete', item_id=1),
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 422
        assert data == {
            'message': 'Item not found',
            'status_code': 422,
        }


def test_items_send__ok(app_test, auth_login):
    user, auth_token = auth_login()
    item = ItemFactory.create(user=user)
    recipient_user = UserFactory.create()

    with app_test.test_client() as client:
        response = client.post(
            url_for('items.ItemSend'),
            data=json.dumps(
                {
                    'item_id': item.id,
                    'recipient_username': recipient_user.username,
                }
            ),
            content_type='application/json',
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 200
        assert 'send_url' in data

        token_data = decode_token(data['send_url'].split('/')[-1])
        assert token_data['sub'] == recipient_user.id
        assert token_data['item_id'] == item.id


def test_items_send__recipient_user_not_found__error(app_test, auth_login):
    user, auth_token = auth_login()
    item = ItemFactory.create(user=user)

    with app_test.test_client() as client:
        response = client.post(
            url_for('items.ItemSend'),
            data=json.dumps(
                {
                    'item_id': item.id,
                    'recipient_username': 'invalid_username',
                }
            ),
            content_type='application/json',
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 422
        assert data == {
            'message': 'User not found',
            'status_code': 422,
        }


def test_items_send__wrong_recipient_user__error(app_test, auth_login):
    user, auth_token = auth_login()
    item = ItemFactory.create(user=user)

    with app_test.test_client() as client:
        response = client.post(
            url_for('items.ItemSend'),
            data=json.dumps(
                {
                    'item_id': item.id,
                    'recipient_username': user.username,
                }
            ),
            content_type='application/json',
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 409
        assert data == {
            'message': 'User already is the owner of the item',
            'status_code': 409,
        }


def test_items_send__item_not_found__error(app_test, auth_login):
    user, auth_token = auth_login()
    recipient_user = UserFactory.create()

    with app_test.test_client() as client:
        response = client.post(
            url_for('items.ItemSend'),
            data=json.dumps(
                {
                    'item_id': 1,
                    'recipient_username': recipient_user.username,
                }
            ),
            content_type='application/json',
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 422
        assert data == {
            'message': 'Item not found',
            'status_code': 422,
        }


def test_items_send_get__ok(
    app_test,
    auth_login,
    send_item_token,
):
    user, auth_token = auth_login()
    item, send_token = send_item_token(user=user)
    old_owner = item.user

    with app_test.test_client() as client:
        response = client.get(
            url_for('items.ItemGetRecipient', send_token=send_token),
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 200
        assert item.user != old_owner
        assert item.user == user
        assert data == {'id': item.id, 'name': item.name, 'user_id': user.id}


def test_items_send_get__failed_link_authentication__error(
    app_test,
    auth_login,
    send_item_token,
):
    user, auth_token = auth_login()
    item, send_token = send_item_token(user=UserFactory.create())

    with app_test.test_client() as client:
        response = client.get(
            url_for('items.ItemGetRecipient', send_token=send_token),
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 401
        assert data == {
            'message': 'Send link failed authentication ',
            'status_code': 401,
        }


def test_items_send_get__user_not_found__error(
    app_test,
    session,
    send_item_token,
):
    user = UserFactory.build(id=2)
    auth_token = user.encode_auth_token()

    item, send_token = send_item_token(user=user)

    with app_test.test_client() as client:
        response = client.get(
            url_for('items.ItemGetRecipient', send_token=send_token),
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 422
        assert data == {
            'message': 'User not found',
            'status_code': 422,
        }


def test_items_send_get__item_not_found__error(
    app_test,
    auth_login,
    send_item_token,
):
    user, auth_token = auth_login()
    item, send_token = send_item_token(user=user, item=ItemFactory.build(id=2))

    with app_test.test_client() as client:
        response = client.get(
            url_for('items.ItemGetRecipient', send_token=send_token),
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
        )
        data = json.loads(response.data.decode())

        assert response.status_code, 422
        assert data == {
            'message': 'Item not found',
            'status_code': 422,
        }
