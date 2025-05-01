import flask
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"

from .views import views

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'able'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')

    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')

    from .models import Note, User  # Import your models here

    with app.app_context():
        db.create_all()

    return app

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print("Database created!")

