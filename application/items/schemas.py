from marshmallow import Schema
from marshmallow import fields

from application.items import models


class NewItemSchema(Schema):
    name = fields.String(description='Name of a new item', required=True)


class ItemSchema(Schema):
    class Meta:
        model = models.Item
        fields = (
            'id',
            'name',
            'user_id',
        )


class SendItemSchema(Schema):
    item_id = fields.Integer(
        description='ID of an element which will be sent', required=True
    )
    recipient_username = fields.String(
        description='Name of a user to whom the item will be sent', required=True
    )
