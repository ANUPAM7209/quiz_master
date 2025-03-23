from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo

#instance of the form class
class RegisterForm(FlaskForm):
    #add the feilds to the form
    username = StringField('Email', validators=[DataRequired() , Email()]) #username field
    password = PasswordField('Password', validators=[Length(min=8)]) #password field
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')]) #confirm password field
    fullname = StringField('Full Name') #fullname field
    qualification = StringField('Qualification') #qualification field
    dob = DateField('Date of Birth', format = '%Y-%m-%d', validators = [DataRequired()]) #date of birth field
    submit = SubmitField('Sign Up') #submit button

class LoginForm(FlaskForm): # instance of the form class
    username = StringField('Email', validators=[DataRequired() , Email()]) #username field
    password = PasswordField('Password', validators=[Length(min=8)]) #password field
    remember = BooleanField('Remember Me') #remember me field
    submit = SubmitField('Login') #submit button


# How we use that form in the routes.py file:
# from app.forms import RegisterForm, LoginForm