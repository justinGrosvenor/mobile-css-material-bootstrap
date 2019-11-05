import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemySessionUserDatastore, UserMixin, RoleMixin, login_required
from app.database import db_session, init_db
from app.models import User, Role 
# from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_security.forms import RegisterForm, LoginForm
from wtforms import Form, BooleanField, StringField, validators

app = Flask(__name__)
app.config['GOOGLE_MAPS_KEY'] = "AIzaSyC8KwSFZbAdmiv4Km6tfPa8Q2Ugw5tZqJM"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = "0xff7"
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_TRACKABLE'] = True
# app.config['MAIL_SERVER'] = 'localhost'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = 'username'
# app.config['MAIL_PASSWORD'] = 'password'
# app.config['SECURITY_EMAIL_SENDER'] = 'noreply@gmail.com'

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
# mail = Mail(app)
# Bootstrap(app)

@app.before_first_request
def create_user():
    init_db()
    user_datastore.create_user(email='matt@nobien.net', password='password')
    db_session.commit()

class Reg_Form(RegisterForm):
	username = StringField('User Name')

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore, register_form=Reg_Form)

from app import views

