#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 13:13:49 2019

@author: RamanSB
"""

import os

from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager 


#Initializing all flask extensions
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = "log the fuck in"

#Factory method to create Flask app instance
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class) #Setting app configuration 
    
    db.init_app(app) #Initializing db with app
    migrate.init_app(app, db) #Initializing migrate w/App+db
    login.init_app(app)
    bootstrap.init_app(app)
    
    
    #Need to register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    
    
    
    return app

from app import models