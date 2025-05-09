import flask
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
import os  # Import os to access environment variables

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"

from .views import views

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("able", "default_secret_key")  # Use environment variable
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    from .models import Note, User, SharedPost  # Import your models here

    with app.app_context():
        db.create_all()

    @app.context_processor
    def inject_unseen_count():
        user_id = session.get('user_id')
        unseen_count = 0
        if user_id:
            unseen_count = SharedPost.query.filter_by(recipient_id=user_id, seen=False).count()
        return dict(unseen_count=unseen_count)

    return app

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print("Database created!")