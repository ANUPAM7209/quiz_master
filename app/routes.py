from app import create_app , db , login_manager
from flask import render_template , url_for , redirect , flash , request
from app.models import User, Subject, Chapter, Question,  Quiz , Score
from app.forms import RegisterForm, LoginForm , SubjectForm , ChapterForm , QuizForm
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

#CRUD operations for the subject
#add the subject
@app.route("/admin/add_subject" , methods = ['GET' , 'POST'])
@login_required
def add_subject():
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home'))
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(
            name = form.name.data,
            description = form.description.data
        )#create the subject object
        db.session.add(subject) #add the subject object to the session, store the object in the database
        db.session.commit() #commit the session
        flash('Subject added successfully!' , category='success')
        return redirect(url_for('manage_subjects')) #redirect to the manage_subjects page
    return render_template('admin/add_subject.html' , form = form)

#edit the subject
@app.route("/admin/edit_subject/<int:id>" , methods = ['GET' , 'POST'])
@login_required
def edit_subject(id):
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home'))
    subject = Subject.query.get_or_404(id) #fetch the subject object from the database, if the object is not present then return 404
    form = SubjectForm(obj=subject) #create the instance of the form , initialize the form object , fill the form with the data
    if form.validate_on_submit():
        #update the subject object
        subject.name = form.name.data
        subject.description = form.description.data
        db.session.commit() #commit the session
        flash('Subject updated successfully!' , category='success')
        return redirect(url_for('manage_subjects')) #redirect to the manage_subjects page
    return render_template('admin/edit_subject.html' , form = form)


#delete the subject
@app.route("/admin/delete_subject/<int:id>" , methods = ['POST']) #id is the primary key of the subject object
@login_required
def delete_subject(id):
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home'))
    subject = Subject.query.get_or_404(id) #fetch the subject object from the database, if the object is not present then return 404
    db.session.delete(subject) #delete the subject object
    db.session.commit() #commit the session
    flash('Subject deleted successfully!' , category='success')
    return redirect(url_for('manage_subjects')) #redirect to the manage_subjects page


@app.route('/admin/manage_chapters')
@login_required
def manage_chapters():
    if current_user.username != os.getenv('ADMIN_USERNAME'): #check if the current user is the admin user or not
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home')) #redirect to the home page
    chapters = Chapter.query.all()
    return render_template('admin/manage_chapters.html' , chapters = chapters)

#CRUD operations for the chapters
#add the chapter
@app.route("/admin/add_chapter" , methods = ['GET' , 'POST'])
@login_required
def add_chapter():
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home'))
    form = ChapterForm()
    form.subject_id.choices = [(s.id , s.name) for s in Subject.query.all()] #fetch the subject id and the subject name from the database
    if form.validate_on_submit():
        chapter = Chapter(
            name = form.name.data,
            description = form.description.data,
            subject_id = form.subject_id.data
        )
        db.session.add(chapter) #add the chapter object to the session
        db.session.commit() #commit the session
        flash('Chapter added successfully!' , category='success')
        return redirect(url_for('manage_chapters')) #redirect to the manage_chapters page
    return render_template('admin/add_chapter.html' , form = form)

#edit the chapters
@app.route("/admin/edit_chapter/<int:id>" , methods = ['GET' , 'POST'])
@login_required
def edit_chapter(id):
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home'))
    chapter = Chapter.query.get_or_404(id) #fetch the chapter object from the database, if the object is not present then return 404
    form = ChapterForm(obj=chapter) #create the instance of the form , initialize the form object , fill the form with the data
    form.subject_id.choices = [(s.id , s.name) for s in Subject.query.all()] #fetch the subject id and the subject name from the database
    if form.validate_on_submit():
        #update the chapter object
        chapter.name = form.name.data
        chapter.description = form.description.data
        chapter.subject_id = form.subject_id.data
        db.session.commit()
        flash('Chapter updated successfully!' , category='success')
        return redirect(url_for('manage_chapters')) #redirect to the manage_chapters page
    return render_template('admin/edit_chapter.html' , form = form)

#delete the chapter
@app.route("/admin/delete_chapter/<int:id>" , methods = ['POST']) #id is the primary key of the chapter object
@login_required
def delete_chapter(id): 
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home'))
    chapter = Chapter.query.get_or_404(id)
    db.session.delete(chapter) #delete the chapter object
    db.session.commit() #commit the session
    flash('Chapter deleted successfully!' , category='success')
    return redirect(url_for('manage_chapters')) #redirect to the manage_chapters page


@app.route('/admin/manage_quizzes')
@login_required
def manage_quizzes():
    if current_user.username !=os.getenv('ADMIN_USERNAME'): #check if the current user is the admin user or not
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home')) #redirect to the home page
    quizzes = Quiz.query.all()
    return render_template('admin/manage_quizzes.html' , quizzes = quizzes) # fetch the data and supply to the params

#CRUD operations for the quizzes
#add the quiz
@app.route("/admin/add_quiz" , methods = ['GET' , 'POST'])
@login_required
def add_quiz(): 
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home'))
    form = QuizForm()
    form.chapter_id.choices = [(c.id , c.name) for c in Chapter.query.all()] #fetch the chapter id and the chapter name from the database
    if form.validate_on_submit():
        quiz = Quiz(
            date_of_quiz = form.date_of_quiz.data,
            time_duration = form.time_duration.data,
            chapter_id = form.chapter_id.data
        )
        db.session.add(quiz) #add the quiz object to the session
        db.session.commit() #commit the session
        flash('Quiz added successfully!' , category='success')
        return redirect(url_for('manage_quizzes')) #redirect to the manage_quizzes page
    return render_template('admin/add_quiz.html' , form = form)

#edit the quiz
@app.route("/admin/edit_quiz/<int:id>" , methods = ['GET' , 'POST'])
@login_required
def edit_quiz(id):
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home'))
    quiz = Quiz.query.get_or_404(id) #fetch the quiz object from the database, if the object is not present then return 404
    form = QuizForm(obj=quiz) #create the instance of the form , initialize the form object , fill the form with the data
    form.chapter_id.choices = [(c.id , c.name) for c in Chapter.query.all()] #fetch the chapter id and the chapter name from the database
    if form.validate_on_submit():    
        #update the quiz object
        quiz.name = form.name.data
        quiz.date_of_quiz = form.date_of_quiz.data
        quiz.time_duration = form.time_duration.data
        quiz.chapter_id = form.chapter_id.data
        db.session.commit()
        flash('Quiz updated successfully!' , category='success')
        return redirect(url_for('manage_quizzes')) #redirect to the manage_quizzes page
    return render_template('admin/edit_quiz.html' , form = form)

#delete the quiz
@app.route("/admin/delete_quiz/<int:id>" , methods = ['POST']) #id is the primary key of the quiz object
@login_required
def delete_quiz(id):
    if current_user.username != os.getenv('ADMIN_USERNAME'):
        flash('You are not authorized to view this page!' , category='error')
        return redirect(url_for('home'))
    quiz = Quiz.query.get_or_404(id) #fetch the quiz object from the database, if the object is not present then return 404
    db.session.delete(quiz) #delete the quiz object
    db.session.commit() #commit the session
    flash('Quiz deleted successfully!' , category='success')
    return redirect(url_for('manage_quizzes')) #redirect to the manage_quizzes page     
        
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