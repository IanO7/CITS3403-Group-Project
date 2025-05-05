import flask
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
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

    from .models import Note, User  # Import your models here

    with app.app_context():
        db.create_all()

    return app

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print("Database created!")
        
'''
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='YOUR_GOOGLE_CLIENT_ID',
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params={'prompt': 'consent', 'access_type': 'offline'},
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'}
)

from flask_dance.contrib.google import make_google_blueprint, google

google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_to="google_login"
)
app.register_blueprint(google_bp, url_prefix="/login")
'''


