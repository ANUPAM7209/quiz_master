from app import create_app , db , login_manager
from flask import render_template , url_for , redirect , flash 
from app.models import User, Subject, Chapter, Question, Score, Quiz 
from app.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required

app = create_app() #store the object of the flask app

@login_manager.user_loader #to load the user
def load_user(user_id): #to load the user that is storted in the session
    return User.query.get(int(user_id)) #then we have to return the user object

@app.cli.command('create_db')  # to initlize the database . create the database tables
def create_db(): #handler for about command
    """Create the database tables."""
    with app.app_context():
        db.create_all()
    print('Database created successfully!')

@app.route('/')
def home():
    return render_template('home.html') #render the home.html file in the templates folder

@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    form = RegisterForm() #Read the register form object
    if form.validate_on_submit():
        user = User(username = form.username.data , 
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