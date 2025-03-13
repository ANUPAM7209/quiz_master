from app import create_app , db
from flask import render_template
from app.models import User, Subject, Chapter, Question, Score, Quiz

app = create_app()


@app.cli.command('create_db')  
def create_db():
    """Create the database tables."""
    with app.app_context():
        db.create_all()
    print('Database created successfully!')

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/about')
def about():
    return 'about page'