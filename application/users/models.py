import datetime

from flask_jwt_extended import create_access_token
from passlib.apps import custom_app_context as pwd_context

from application import db


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password: str) -> None:
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    def encode_auth_token(self, expiration: int = 600) -> str:
        return create_access_token(
            identity=self.id, expires_delta=datetime.timedelta(seconds=expiration)
        )
