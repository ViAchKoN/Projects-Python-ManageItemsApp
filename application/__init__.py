from flask import Flask
from flask import jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

from application.core.errors import CustomException

db = SQLAlchemy(session_options={'autocommit': False})
jwt = JWTManager()


def create_app():
    app = Flask(
        __name__,
    )

    app.config.from_object('application.config.DevelopmentConfig')
    app.config['API_SPEC_OPTIONS'] = {
        'security': [{'bearerAuth': []}],
        'components': {
            'securitySchemes': {
                'bearerAuth': {
                    'type': 'http',
                    'scheme': 'bearer',
                    'bearerFormat': 'JWT',
                }
            }
        },
    }

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)
    api = Api(app)

    from items.views import items_blp
    from users.views import users_blp

    api.register_blueprint(users_blp)
    api.register_blueprint(items_blp)

    @app.errorhandler(CustomException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app
