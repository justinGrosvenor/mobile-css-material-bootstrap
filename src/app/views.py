from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt, Reg_Form
from flask_security import Security, SQLAlchemySessionUserDatastore, UserMixin, RoleMixin, login_required, roles_required
from flask_security.forms import RegisterForm, LoginForm
from app.models import User, Role
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user
from datetime import datetime


class AdminIndex(AdminIndexView):
    def is_accessible(self):
        # if current_user:
        #     return current_user.has_role('admin')
        # else:
        # 	return False
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/')

admin = Admin(app, name='admin', index_view=AdminIndex())
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = Reg_Form()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('account created', 'success')
        return redirect('/login')
    return render_template('/security/register_user.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = user.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user)
        return redirect('/')
    else:
        flash('Login Unsuccessful. Please try again', 'danger')
    return render_template('/security/login_user.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


