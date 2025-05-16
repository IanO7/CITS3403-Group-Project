import flask
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from os import path
import os  # Import os to access environment variables
from datetime import timedelta  # Import timedelta for session configuration
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
DB_NAME = "database.db"
csrf = CSRFProtect()

from .views import views

def create_app():
    app = Flask(__name__)
    # TODO: Change this to a secure key before deployment
    # For development only - do not use this in production!
    app.config['SECRET_KEY'] = os.environ.get("able", "default_secret_key")
    
    # Add session configuration
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate

    # Initialize CSRF protection
    csrf.init_app(app)

    # Initialize Flask-Login with stronger configuration
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'
    login_manager.refresh_view = 'auth.login'
    login_manager.needs_refresh_message = 'Please login again to verify your identity'


    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        if not user_id or user_id == 'None':
            return None
        try:
            return User.query.get(int(user_id))
        except (ValueError, TypeError):
            return None

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