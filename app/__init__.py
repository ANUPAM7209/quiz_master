from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager

db = SQLAlchemy() #intialize the database
login_manager = LoginManager() #initialize the login manager

def create_app():
    app = Flask(__name__) # runnig the current module . not importing the module
    app.config['SECRET_KEY'] = 'secret_key' #secret key for the form , for development purpose we use this key other wize we use the os.urandom(16) to generate the random key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db' #intract with the database ,where is your database located
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #disable the modification tracking


    db.init_app(app) #initialize the database connect the app with the database
    login_manager.init_app(app) #initialize the login manager

    
    return app #return the app object
