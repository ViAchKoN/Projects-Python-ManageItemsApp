from flask import jsonify
from flask import make_response
from flask.views import MethodView
from flask_smorest import Blueprint

from application import db
from application.core import errors
from application.users import models

from . import schemas

users_blp = Blueprint('users', 'users', url_prefix='/users', description='Operations on users')


@users_blp.route('/registration')
class UserRegistration(MethodView):
    @users_blp.arguments(schemas.UserRegistrationSchema)
    @users_blp.response(200, schemas.UserSchema)
    def post(self, user_registration_data):
        username: str = user_registration_data['username']
        password: str = user_registration_data['password']
        if models.User.query.filter_by(username=username).first():
            raise errors.UserAlreadyExists()
        user = models.User(username=username)
        user.hash_password(password)

        db.session.add(user)
        db.session.commit()
        return user


@users_blp.route('/login')
class UserLogIn(MethodView):
    @users_blp.arguments(schemas.UserLogInSchema)
    def post(self, user_login_data):
        username: str = user_login_data['username']
        password: str = user_login_data['password']
        user = models.User.query.filter_by(username=username).first()

        if user is None:
            raise errors.UserNotFound()

        if user.verify_password(password=password):
            auth_token = user.encode_auth_token()
            responseObject = {'auth_token': auth_token}
            return make_response(jsonify(responseObject), 200)
        else:
            raise errors.WrongCredentials()
