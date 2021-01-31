import os, re
from flask import Flask, url_for, render_template, redirect, flash, request, jsonify, session
from forms.forms import TwitterForm, FeedbackForm, RegistrationForm, LoginForm, GuessTheWordForm
import json
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from flask_mail import Mail
from brain.tweet_analysis import tweet_analysis_function
from config.config import RC_SITE_KEY, RC_SECRET_KEY, SECRET_KEY, SQLALCHEMY_DATABASE_URI

app=Flask(__name__)

app.config['SECRET_KEY']=SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI']=SQLALCHEMY_DATABASE_URI
app.config['RECAPTCHA_PUBLIC_KEY']=RC_SITE_KEY
app.config['RECAPTCHA_PRIVATE_KEY']=RC_SECRET_KEY

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Feedback(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    feedback=db.Column(db.String())
    email=db.Column(db.String())
    
    def __repr__(self):
        return f"Feedback('{self.id}','{self.feedback}','{self.email}')"

class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),nullable=False,unique=True)
    email=db.Column(db.String(),nullable=False,unique=True)
    username=db.Column(db.String(30),nullable=False,unique=True)
    password=db.Column(db.String(30),nullable=False)
    
    def __repr__(self):
        return f"User('{self.id}','{self.username}','{self.email}')"


@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def home():
    user=" "
    if current_user.is_authenticated:
        user=current_user.username
    return render_template('home.html',title="Home",user=user)

@app.route('/about')
def about():
    return render_template('about.html',title="About")

@app.route('/movie_analysis',methods=['GET','POST'])
def movie_analysis():
    count_sentiment=0
    form=TwitterForm()
    if request.method=="POST":
        hashtag=form.hashtag.data
        #flash(f'Analysing Tweets... Please wait...','success')
        count_sentiment=tweet_analysis_function(hashtag)
        return redirect(url_for('movie_analysed',count_sentiment=count_sentiment,_external=True))
    return render_template('movie_analysis.html',title="Movie Analysis",form=form)

@app.route('/movie_analysed/<count_sentiment>')
def movie_analysed(count_sentiment):
    count_sentiment=eval(count_sentiment)
    i=count_sentiment['count_positive']+count_sentiment['count_neutral']+count_sentiment['count_negative']
    c_pos=round(100.00*count_sentiment['count_positive']/(i),2)
    c_neu=round(100.00*count_sentiment['count_neutral']/(i),2)
    c_neg=round(100.00*count_sentiment['count_negative']/(i),2)
    movie_name=count_sentiment['movie_name']
    return render_template('movie_analysed.html',title="Movie Analysis",c_pos=c_pos,c_neu=c_neu,c_neg=c_neg,movie_name=movie_name)

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if current_user.is_authenticated:
        flash(f'You are already loggedin as {current_user.username}. Logout to Register a new User','info')
        return redirect(url_for('home',title="Home",_external=True))
    if request.method=="POST":
        if not User.query.filter_by(username=form.username.data).first():
            if not User.query.filter_by(email=form.email.data).first():
                hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user=User(username=form.username.data,email=form.email.data,password=hashed_password)
                db.session.add(user)
                db.session.commit()
                flash(f'Account successfully created for the email: { user.email.data }','success')
                return redirect(url_for('login',title='Login',form=form,_external=True))
            else:
                flash(f'The Email { form.email.data } is already taken. Please use a different email id.','danger')
                return redirect(url_for('register',title='Login',form=form,_external=True))
        else:
            flash(f'The Username {form.username.data } is already taken. Please use a different username.','danger')
            return redirect(url_for('register',title="Register",form=form,_external=True))
    else:
        return render_template('register.html',title="Register",form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if current_user.is_authenticated:
        flash(f'You are already loggedin as {current_user.username}.','info')
        return redirect(url_for('home',title="Home",_external=True))
    if request.method=="POST":
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                flash(f'Welcome, { user.username }!','success')
                return redirect(url_for('home',title="Home",_external=True))
            else:
                flash(f'Incorrect Password. Try again!','danger')
                return redirect(url_for('login',title="Login",form=form,_external=True))
        else:
            flash(f'Incorrect Email. Try again!','danger')
            return redirect(url_for('login',title="Login",form=form,_external=True))
    return render_template('login.html',title="Login",form=form)

@app.route('/logout',methods=['GET','POST'])
def logout():
    if current_user.is_authenticated:
        session.clear()
        logout_user()
        flash(f'Loggedout Successfully.','success')
        return redirect(url_for('home',title="Home",_external=True))
    flash(f'Already loggedout.')
    return render_template('home.html',title="Home",_external=True)

@app.route('/guess_the_word',methods=['GET','POST'])
def guess_the_word():
    return render_template('guess_the_word.html',title="Guess the word")

@app.route('/feedback',methods=['GET','POST'])
def feedback():
    form=FeedbackForm()
    if request.method=="POST":
        regex_email=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        regex_feedback=r"(^[\S\s]{10,200})"
        
        if re.match(regex_email,form.email.data):
            if re.match(regex_feedback,form.feedback.data):
                feedback=Feedback(feedback=form.feedback.data,email=form.email.data)
                db.session.add(feedback)
                db.session.commit()
                flash(f'Thank you for the Feedback!','success')
                return redirect(url_for('home',title="Home",_external=True))
            else:
                flash(f'Please enter 10-200 characters for feedback and a valid email id!','danger')
                return redirect(url_for('feedback',title="Home",_external=True))
        else:
            flash('Please enter 10-200 characters for feedback and a valid email id!','danger')
            return redirect(url_for('feedback',title="Home",_external=True))
    return render_template('feedback.html',title="Feedback",form=form)

@app.route('/feedback_results')
def feedback_results():
    feedback=Feedback.query.all()
    return render_template('feedback_results.html',title="Feedback",feedback=feedback)

@app.route('/testlogin',methods=['GET','POST'])
def testlogin():
    form=LoginForm()
    if current_user.is_authenticated:
        return f"You are already logged in as {current_user.username}"
    elif request.method=="POST":
        if form.email.data:
            if form.password.data:
                user=User.query.filter_by(email=form.email.data).first()
                if user:
                    if bcrypt.check_password_hash(user.password,form.password.data):
                        if login_user(user):
                            return f"User {current_user.username} loggedin"
                        else:
                            return "User exists but not loggedin"
                        return "User exists and Password Matches"
                    else:
                        return "User exists but Password doesn't match"
                else:
                    return "User Does not exist"
                return f"Password:{form.password.data}"
            else:
                return "Password failed"
            return f"Email: {form.email.data}!"
        else:
            return "Email failed"
        return "POST Verified"
    #return render_template('login.html',title="Home",_external=True,form=form)
    return "GET Verfied"

if __name__ == "__main__":
    app.run(debug=True,port=8000)