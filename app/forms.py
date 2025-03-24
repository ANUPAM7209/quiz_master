from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField , TextAreaField , SelectField , IntegerField , DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo

#instance of the form class
class RegisterForm(FlaskForm):
    #add the feilds to the form
    username = StringField('Email', validators=[DataRequired() , Email()]) #username field
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)]) #password field
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')]) #confirm password field
    fullname = StringField('Full Name') #fullname field
    qualification = StringField('Qualification') #qualification field
    dob = DateField('Date of Birth', format = '%Y-%m-%d', validators = [DataRequired()]) #date of birth field
    submit = SubmitField('Sign Up') #submit button

class LoginForm(FlaskForm): # instance of the form class
    username = StringField('Email', validators=[DataRequired() , Email()]) #username field
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)]) #password field
    remember = BooleanField('Remember Me') #remember me field
    submit = SubmitField('Login') #submit button

class SubjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()]) #name field
    description = TextAreaField('Description') #description field
    submit = SubmitField('submit') #submit button

class ChapterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()]) #name field
    description = TextAreaField('Description') #description field
    subject_id = SelectField('Subject' , coerce= int , validators=[DataRequired()]) #subject id field ,show the relationship between the chapter and the subject , coerce -> convert the value into the integer
    submit = SubmitField('submit') #submit button

class QuizForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()]) #name field
    date_of_quiz = DateTimeLocalField('Date of Quiz',validators=[DataRequired()]) #date of quiz field
    time_duration = IntegerField('Time Duration (In seconds)', validators=[DataRequired()]) #time duration field
    chapter_id = SelectField('Chapter', coerce= int , validators=[DataRequired()]) #chapter id field , show the relationship between the quiz and the chapter , coerce -> convert the value into the integer
    submit = SubmitField('submit') #submit button



















# How we use that form in the routes.py file:
# from app.forms import RegisterForm, LoginForm