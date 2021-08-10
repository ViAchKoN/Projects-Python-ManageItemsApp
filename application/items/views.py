import datetime

from flask import jsonify
from flask import make_response
from flask import url_for
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from flask_jwt_extended import decode_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint

from application import db
from application.core import errors
from application.items import models
from application.items import schemas
from application.users import models as user_models

items_blp = Blueprint('items', 'items', url_prefix='/items', description='Operations on items')


@items_blp.route('/new')
class ItemAdd(MethodView):
    @items_blp.arguments(schemas.NewItemSchema)
    @items_blp.response(200, schemas.ItemSchema)
    @jwt_required()
    def post(self, new_item_data):
        name: str = new_item_data['name']
        user = user_models.User.query.filter_by(id=get_jwt_identity()).first()
        if user is None:
            raise errors.UserNotFound()
        item = models.Item(name=name, user=user)
        db.session.add(item)
        db.session.commit()
        return item


@items_blp.route('/')
class ItemListGet(MethodView):
    @items_blp.response(200, schemas.ItemSchema(many=True))
    @jwt_required()
    def get(self):
        user = user_models.User.query.filter_by(id=get_jwt_identity()).first()
        if user is None:
            raise errors.UserNotFound()
        items = models.Item.query.filter_by(user=user).all()
        return items


@items_blp.route('/<item_id>')
class ItemDelete(MethodView):
    @jwt_required()
    def delete(self, item_id):
        user = user_models.User.query.filter_by(id=get_jwt_identity()).first()
        if user is None:
            raise errors.UserNotFound()

        item = models.Item.query.filter_by(id=item_id, user_id=get_jwt_identity()).first()
        if item is None:
            raise errors.ItemNotFound()

        db.session.delete(item)
        db.session.commit()

        responseObject = {
            'message': 'ok',
            'status_code': 200,
        }
        return make_response(jsonify(responseObject), 200)


@items_blp.route('/send')
class ItemSend(MethodView):
    @items_blp.arguments(schemas.SendItemSchema)
    @jwt_required()
    def post(self, send_item_data):
        item_id: str = send_item_data['item_id']
        recipient_username: str = send_item_data['recipient_username']

        recipient_user = user_models.User.query.filter_by(username=recipient_username).first()
        if recipient_user is None:
            raise errors.UserNotFound()

        if recipient_user.id == get_jwt_identity():
            raise errors.WrongRecipientUser()

        item = models.Item.query.filter_by(id=item_id, user_id=get_jwt_identity()).first()
        if item is None:
            raise errors.ItemNotFound()

        send_token = create_access_token(
            recipient_user.id,
            additional_claims={'item_id': item_id},
            expires_delta=datetime.timedelta(hours=2),
        )
        responseObject = {'send_url': url_for('items.ItemGetRecipient', send_token=send_token, _external=True)[:-3]}
        return make_response(jsonify(responseObject), 200)


@items_blp.route('/<send_token>}')
class ItemGetRecipient(MethodView):
    @items_blp.response(200, schemas.ItemSchema)
    @jwt_required()
    def get(self, send_token):
        token_data = decode_token(send_token)
        request_user_id = get_jwt_identity()

        if token_data['sub'] != request_user_id:
            raise errors.UnauthorizedSendLink()

        user = user_models.User.query.filter_by(id=request_user_id).first()
        if user is None:
            raise errors.UserNotFound()

        item = models.Item.query.filter_by(id=token_data['item_id']).with_for_update(of=models.Item).first()
        if item is None:
            raise errors.ItemNotFound()

        item.user = user
        db.session.commit()

        return item
