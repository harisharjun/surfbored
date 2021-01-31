from flask_wtf import FlaskForm, RecaptchaField, Form
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class TwitterForm(FlaskForm):
    hashtag=StringField('Enter the movie hashtag (include the # sign):',validators=[DataRequired(),Length(min=2)])
    #recaptcha = RecaptchaField()
    submit=SubmitField('Analyse')

class FeedbackForm(FlaskForm):
    feedback=TextAreaField('What should I add to this portal?', validators=[DataRequired(),Length(min=10,max=250)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    #recaptcha = RecaptchaField()
    submit=SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(),Length(min=1,max=30)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    #recaptcha = RecaptchaField()
    submit=SubmitField('Register')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    #remember=BooleanField('Remember')
    #recaptcha = RecaptchaField()
    submit=SubmitField('Login')

class GuessTheWordForm(FlaskForm):
    submit=SubmitField('Submit')