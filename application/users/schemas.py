from marshmallow import Schema
from marshmallow import ValidationError
from marshmallow import fields
from marshmallow import validates_schema


class UserRegistrationSchema(Schema):
    username = fields.String(description='Username for account', required=True)
    password = fields.String(description='Password for account', required=True)
    password_confirmation = fields.String(
        description='Confirmation of password', required=True
    )

    @validates_schema
    def validate(self, data, **kwargs):
        if data['password'] != data['password_confirmation']:
            raise ValidationError('Passwords are not identical')


class UserSchema(Schema):
    class Meta:
        fields = (
            'id',
            'username',
        )


class UserLogInSchema(Schema):
    username = fields.String(description='Username for account', required=True)
    password = fields.String(description='Password for account', required=True)
