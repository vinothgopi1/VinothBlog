from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from typing import Optional
from datetime import datetime
import startup 


app = startup.get_app()
db = startup.get_db()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def getID(name):
    temp = (User.query.filter_by(name = name).all())
    return(temp.id)

#database that stores blogposts
class BlogT(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True, nullable = False, autoincrement = True)
    id = db.Column(db.Integer, nullable = True)
    name = db.Column(db.String(100), nullable = True)
    title = db.Column(db.String(100), nullable = False)
    body = db.Column(db.String(100000), nullable = False)
    time = db.Column(db.String(100), nullable = False)

#database that stores users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)

with app.app_context():
    print("********** ALL TABLES ARE CREATED ****************")
    db.create_all()


#Registration Form
class RegisterForm(FlaskForm):
    username = StringField(validators = [InputRequired(), Length(min = 1, max = 20)], render_kw = {"placeholder": "Username"})
    password = PasswordField(validators = [InputRequired(), Length(min = 1, max = 20)], render_kw = {"placeholder": "Password"})

    submit = SubmitField("Register")
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username = username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please choose different one")
#Login Form
class LoginForm(FlaskForm):
    username = StringField(validators = [InputRequired(), Length(min = 1, max = 20)], render_kw = {"placeholder": "Username"})
    password = PasswordField(validators = [InputRequired(), Length(min = 1, max = 20)], render_kw = {"placeholder": "Password"})

    submit = SubmitField("Login")



