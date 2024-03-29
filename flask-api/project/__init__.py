from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from .db import db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///app.db',
        SECRET_KEY="secret key goes here!",
        # SQLALCHEMY_ENGINE_OPTIONS={'sqlite3': {'check_same_thread': False, 'detect_types': sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES, 'foreign_keys': True}}
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    )
    app.url_map.strict_slashes = False

    db.init_app(app)
    CORS(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    bycript = Bcrypt(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when testing
        app.config.from_pyfile("./config/config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # registering routes
    from .routes import auth
    app.register_blueprint(auth.bp)

    from .routes import customers
    app.register_blueprint(customers.bp)

    from .routes import devices
    app.register_blueprint(devices.bp)

    from .routes import home
    app.register_blueprint(home.bp)

    # return the configured app instance
    return app
