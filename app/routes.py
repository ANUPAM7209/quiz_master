from app import create_app , db , login_manager
from flask import render_template , url_for , redirect , flash 
from app.models import User, Subject, Chapter, Question,  Quiz , Score
from app.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required , current_user
import os

app = create_app() #store the object of the flask app

@login_manager.user_loader #to load the user
def load_user(user_id): #to load the user that is storted in the session
    return User.query.get(int(user_id)) #then we have to return the user object

@app.cli.command('create_db')  # to initlize the database . create the database tables
def create_db(): #handler for about command
    """Create the database tables."""
    db.create_all() #create the database tables
    print('Database created successfully!')

        #create the admin user
    admin = User.query.filter_by(username=os.getenv('ADMIN_USERNAME')).first() #check if the admin user is already created or not
    if not admin: #if the admin user is not created then create the admin user
            admin = User(
                username = os.getenv('ADMIN_USERNAME'),
                fullname = 'Quiz master Admin'

            )
            admin.set_password(os.getenv('ADMIN_PASSWORD'))#set the password for the admin user
            db.session.add(admin)#add the admin user to the session
            db.session.commit()#commit the session
            print ('Admin user created successfully!')
    else:
            print ('Admin user already exists!')
    print('Database created successfully!')

@app.route('/')
def home():
    return render_template('home.html') #render the home.html file in the templates folder

@app.route('/admin/login' , methods = ['GET' , 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():#check if the form is submitted or not
        user = User.query.filter_by(username = os.getenv('ADMIN_USERNAME')).first() #fetch the user from the database
        if user and user.username == form.username.data and user.check_password(form.password.data): #check if the user is present in the database and the password is correct or not
            login_user(user) #create the session for the user
            flash(f'Login successful for {form.username.data}!' , category='success')
            return redirect(url_for('admin_dashboard')) #generate the url for the admin dashboard convert the string into the url
        else:
            flash('Login Unsuccessful. Please check username and password' , category='error')
    return render_template('admin/login.html' , form = form) #render the login.html file in the templates folder

@app.route('/admin/dashboard')
@login_required #to check the user is logged in or not
def admin_dashboard():
    if current_user.username != os.getenv('ADMIN_USERNAME'): #check if the current user is the admin user or not
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home')) #redirect to the home page
    return render_template('admin/dashboard.html')

@app.route('/admin/manage_subjects')
@login_required
def manage_subjects():
    if current_user.username != os.getenv('ADMIN_USERNAME'): #check if the current user is the admin user or not
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home')) #redirect to the home page
    subjects =  Subject.query.all()
    return render_template('admin/manage_subjects.html' , subjects = subjects)

@app.route('/admin/manage_chapters')
@login_required
def manage_chapters():
    if current_user.username != os.getenv('ADMIN_USERNAME'): #check if the current user is the admin user or not
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home')) #redirect to the home page
    chapters = Chapter.query.all()
    return render_template('admin/manage_chapters.html' , chapters = chapters)

@app.route('/admin/manage_quizzes')
@login_required
def manage_quizzes():
    if current_user.username !=os.getenv('ADMIN_USERNAME'): #check if the current user is the admin user or not
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home')) #redirect to the home page
    quizzes = Quiz.query.all()
    return render_template('admin/manage_chapters.html' , quizzes = quizzes) # fetch the data and supply to the params
        
@app.route('/admin/manage_questions')
@login_required
def manage_questions():
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home'))
    questions = Question.query.all()
    return render_template('admin/manage_questions.html' , questions= questions)

@app.route('/admin/manage_users')
@login_required
def manage_users():
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home'))
    users = User.query.all()
    return render_template('admin/manage_users.html' , users = users)

@app.route('/admin/manage_scores')
@login_required
def manage_scores():
    if current_user.username !=os.getenv('ADMIN_USERNAME'):
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home'))
    scores = Score.query.all()
    return render_template('admin/manage_scores.html' , scores = scores)


@app.route('/register' , methods = ['GET' , 'POST'])
def register(): 
    form = RegisterForm() #Read the register form object
    if form.validate_on_submit():
        user = User(
            username = form.username.data , 
            fullname = form.fullname.data ,
            qualification = form.qualification.data ,
            dob = form.dob.data
        ) #create the user object
        user.set_password(form.password.data) #once this  function will called to the instnace of the user object the password will be hashed
        db.session.add(user) #add the user object to the session
        db.session.commit() #commit the session , save the user object to the database
        flash(f'Account created for {form.username.data}!' , category='success')
        return redirect(url_for("login")) #redirect to the login page after successful registration.
    return render_template('register.html' , form = form) #render the register.html file in the templates folder

@app.route('/login' , methods = ['GET' , 'POST'])
def login():
    #create an instance of the login form
    form = LoginForm()
    #render the login.html file in the templates folder
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user) # creating the session for the user in our server.
            flash(f'Login successful for {form.username.data}!' , category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password' , category='danger')
    return render_template('login.html' , form = form)

@app.route('/dashboard')
@login_required #to check the user is logged in or not .
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user() #destroy the session for the user
    flash('You have been logged out!' , category='success')
    return redirect(url_for('login'))