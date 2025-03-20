from app import create_app , db
from flask import render_template , url_for
from app.models import User, Subject, Chapter, Question, Score, Quiz 

app = create_app() #store the object of the flask app


@app.cli.command('create_db')  # to initlize the database . create the database tables
def create_db(): #handler for about command
    """Create the database tables."""
    with app.app_context():
        db.create_all()
    print('Database created successfully!')

@app.route('/')
def home():
    return render_template('home.html') #render the home.html file in the templates folder

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')