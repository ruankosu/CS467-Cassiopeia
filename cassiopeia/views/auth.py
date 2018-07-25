import functools
import os
import sys
from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
# Helps handle user sessions
from flask_login import login_user, current_user, logout_user, login_required
from cassiopeia.models.models import User
from cassiopeia import db, global_bcrypt
from cassiopeia.views.signup_forms import (RegistrationForm, LoginForm)


auth = Blueprint('auth', __name__)


# Routes
@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        # URL may need to be altered to correct location
        return redirect('/')
    form = RegistrationForm(request.form)
    mysql = db.get_db()
    if form.validate_on_submit():
        # Hash password
        hashed_pw = global_bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create new user
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        mysql.session.add(user)
        mysql.session.commit()
        # Log in the user
        login_user(user)
        flash('Account has been created! You are now logged in. Please set your preferences now.', 'success')
        # Redirect to preferences dialogue
        return redirect(url_for('signup.language', user_id=user.id))
    return render_template('signup/signup.html', title='Sign Up', form=form)



@auth.route("/login", methods=['GET', 'POST'])
def login():
    db.get_db()
    if current_user.is_authenticated:
        # URL may need to be altered to correct location
        return redirect(url_for('content.index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and global_bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('content.index'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Log In', form=form)

@auth.route("/logout")
def logout():
    logout_user()
    # The following URL may need to be updated for correct routing ***
    return redirect('/')


'''@auth.route("/user_agreement")
   @auth.route("/forgot_password")'''

