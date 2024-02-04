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
    app.config['SECRET KEY'] = 'klajsfdksdfjaskfjhs'
    # create database path
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + DB_NAME
    # initialise the database
    db.init_app(app)
    # register all blueprints
    # ******
    # create database
    create_database(app)
    
    return app

def create_database(app):
    """create the database
    """
    if not path.exists("market/" + DB_NAME):
        with app.app_context():
            db.create_all()
    
