import flask
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from os import path

db = SQLAlchemy()
DB_NAME = "database.db" 

def create_app(): 
    app = Flask(__name__) 
    app.config['SECRET KEY'] = "able" 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
        # secure signing for sessions & flash messages
    app.config['SECRET_KEY'] = 'replace-with-a-random-secret'



    from .views import views 
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Review, User

    with app.app_context():
        db.create_all()

    return app

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print("create database")

