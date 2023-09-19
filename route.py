from flask import redirect, url_for, render_template, session,flash, request
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from typing import Optional
from datetime import datetime
from flask_bcrypt import Bcrypt
#from sqlmodel import Field, SQLMode
import pdb
from datetime import datetime
from blogdb import LoginForm, RegisterForm, User, BlogT
import startup

app = startup.get_app()
bcrypt = startup.get_crypt()
db = startup.get_db()


#displays home page when first loading website
@app.route('/', methods = ['get', 'post'])
def newhome():
    return render_template('newhome.html')



@app.route('/login2', methods = ['get', 'post'])
def login():
    return render_template('home.html')


#creates and displays login form
@app.route("/login", methods = ['get', 'post'])
def home():
    form = LoginForm()
    print(form.username)
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)

                flash("you are successfuly logged in", 'info')
                
                return render_template('blogpage.html',  user = form.username.data)
            else:
                flash("incorrect username or password")
                return render_template('home.html', loginform = form)
    return render_template("home.html", loginform = form)


#navbar home button
@app.route('/home', methods = ['get', 'post'])
def goHome():
    return render_template('newhome.html')


#creates and dipslays register form
@app.route("/register", methods = ['get', 'post'])
def register():
    form = RegisterForm()
    print(form)
    print("**********************")
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username = form.username.data, password = hashed_password)
        print(form.username.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        print(current_user.username)
        
        return render_template('blogpage.html')
    else:
        print("FAILED")

    return render_template("register.html", registerform = form)

#displays blogpage / which is the homepage after logging in or registering
@app.route("/blogpage",  methods = ['get', 'post'])
def blogpage():
    return render_template('blogpage.html')


#takes you to the createpost page
@app.route('/create', methods = ['get', 'post'])
def movetocreate():
    return render_template('createpost.html')


#read logged in user's posts
@app.route('/read', methods = ['get', 'post'] )
def movetoread():
    statement = BlogT.query.filter_by(id = current_user.get_id()).all()
    for row in statement:
        print(row.id)
        print(row.title)
        print(row.body)
        print(row.time)
    return render_template('readpost.html',  database = statement)

#read all users posts
@app.route('/all', methods = ['get', 'post'])
def readall():
    statement = BlogT.query.all()
    return render_template('allposts.html', database = statement)


#logout and returns you to home page
@app.route('/logout', methods = ['get', 'post'])
@login_required
def logout():
    logout_user()
    return render_template('newhome.html')
    

#creates post and stores it in database
@app.route('/createpost', methods = ['get', 'post'])
def createpost():
    print('inside createpost')
    new_post = BlogT(id = current_user.get_id(), name = current_user.username, title = request.form['title'], body = request.form['content'], time = str(datetime.today().strftime('%y-%m-%d')))
    print(new_post)
    db.session.add(new_post)
    print('add')
    db.session.commit()
    print('commit?')
    statement = BlogT.query.filter_by(id = current_user.get_id()).all()
    for row in statement:
        print(row.id)
        print(row.title)
        print(row.body)
        print(row.time)
    return render_template('readpost.html', database = statement )


#navbar about button
@app.route('/about', methods = ['get', 'post'])
def about():
    return render_template('about.html')

#navbar contact button
@app.route('/contact', methods = ['get', 'post'])
def contact():
    return render_template('contact.html')

#see your full post form myPosts table
@app.route('/blogdetail/<blog_id>', methods = ['get', 'post'])
def displaybody(blog_id):
    print(blog_id)
    statement = BlogT.query.filter_by(blog_id = blog_id).all()
    print(statement)
    return render_template('displaybody.html', database = statement)

#delete a post
@app.route('/delete/<blog_id>', methods =  ['get', 'post'])
def deletepost(blog_id):
    print(blog_id)
    d = BlogT.query.filter_by(blog_id = blog_id).delete()
    db.session.commit()
    statement = BlogT.query.filter_by(id = current_user.get_id()).all()
    return render_template('readpost.html', database = statement)


#connects to chat room
@app.route('/room', methods = ['get', 'post'])
def room():
    name = request.form['username']
    room = request.form['room']
    return render_template('room.html', name = name, room = room )


#take you to messaging feature / checks for valid username
@app.route('/messaging', methods = ['get', 'post'])
def messaging():
    if request.method == 'POST':
        msgReciever = request.form.get('username')
        if bool(User.query.filter_by(username = msgReciever).first()) == False:
            return render_template('messaging.html', error = 'Please enter valid name')
    return render_template('messaging.html')

