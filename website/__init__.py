from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from pathlib import Path
from dotenv import load_dotenv
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
DB_NAME = "medical.db"

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .views import views
    from .auth import auth
    from .models import User, Providers, Appointments, Locations, VisitPurpose, Specialty

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    create_database(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
