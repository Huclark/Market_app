from os import path
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    # name of app
    app = Flask(__name__)
    # create secret key
    app.config['SECRET_KEY'] = '348ae77e29d4f051960c9288'
    # create database path
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + DB_NAME
    # initialise the database
    db.init_app(app)
    # Import all models and blueprints
    from .models import Item, RegisterForm, User, LoginForm
    from .views import views
    # register all blueprints
    app.register_blueprint(views, url_prefix="/")
    # create database
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "views.login_page"
    login_manager.login_message_category = "info"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        """Loads an existing user
        """
        return User.query.get(int(id))
    
    return app

def create_database(app):
    """create the database
    """
    if not path.exists("market/" + DB_NAME):
        with app.app_context():
            db.create_all()
    
