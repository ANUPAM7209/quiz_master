from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy() #intialize the database

def create_app():
    app = Flask(__name__) # runnig the current module . not importing the module
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db' #intract with the database ,where is your database located
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #disable the modification tracking


    db.init_app(app) #initialize the database connect the app with the database

    
    return app #return the app object
