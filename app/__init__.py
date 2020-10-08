from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
import random
import string

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def gen_sec_key():
    os.environ['SECRET_KEY'] = ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(64)
    )


def create_app():
    gen_sec_key()
    app = Flask(__name__)
    app.config.from_object(Config)
    db_init(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes_bp.login'
    login_manager.login_message = None
    register_blueprints(app)

    return app


def db_init(app):
    from app import models

    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    from .routes import routes_bp

    app.register_blueprint(routes_bp)
