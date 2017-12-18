import os
from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from celery import Celery

from .info import Info
from .services import Services
from .config import Config

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

__version__ = '1.0.0'

app_info = Info()
services = Services()
config = Config()
socketio = SocketIO()
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(DB_PATH):
    app = Flask(__name__)

    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + DB_PATH
    app.config['SECRET_KEY'] = 'Aqewur381!%*'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from . import events

    from .views.index import index_bp
    from .views.login import login_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(login_bp)

    socketio.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    celery = make_celery(app)
    return app
