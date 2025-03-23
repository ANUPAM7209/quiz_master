from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv() #load the environment variables

db = SQLAlchemy() #intialize the database
login_manager = LoginManager() #initialize the login manager

def create_app():
    app = Flask(__name__) # runnig the current module . not importing the module
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') #secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') #database uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #disable the modification tracking


    db.init_app(app) #initialize the database connect the app with the database
    login_manager.init_app(app) #initialize the login manager

    
    return app #return the app object
