import functools
import os
from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from cassiopeia.models.models import db
from cassiopeia.models.models import User
#from cassiopeia import db

# Register database context
# db.get_db()

# Helps handle user sessions
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth', __name__)


# Routes
@auth.route("/register", methods=['POST'])
def register():
    # Confirm username is unique
    username = request.form['username']
    already_taken = User.query.filter_by(username).first()
    if already_taken:
        flash('Username already in use. Please choose a different one.', 'error')
        #return redirect(url_for(''))

    # Confirm email is unique
    email = request.form['inputEmail']
    email_in_use = User.query.filter_by(email).first()
    if email_in_use:
        flash('Email already associated with an account. Please log in or use a different email address.', 'error')
        #return redirect(url_for(''))

    # Confirm registration password matches confirmation password
    # If password != confirmation password, flash error
    password = request.form('inputPassword')
    if password != request.form('confirmPassword'):
        flash('Passwords entered do not match. Please correct and resubmit.', 'error')
        # redirect?

    hashed_pwd = bcrypt.generate_password_hash(request.form('inputPassword')).decode('utf-8')
    new_user = User(username=request.form('username'), email=request.form('inputEmail'), password=hashed_pwd)
    db.session.add(new_user)
    db.session.commit()
    flash('Your account has been created! You are now able to log in', 'success')
    return redirect(url_for('auth.login'))
    return render_template('signup.html', title='Sign Up')


@auth.route("/login", methods=['GET', 'POST'])
def login():
    '''Check if current user is authenticated
        if so, redirect to home page

        else, on form submission and validation,
        Get the username for given email
        If the entered password matches the user's password (ret'd from db)
            login_user for session
        redirect to home
        else flash unsuccessful login message
        render login template'''
    return render_template('auth/login.html', title='Log In')


@auth.route("/logout")
def logout():
    logout_user()
    return
    #return redirect(url_for(''))


'''@auth.route("/user_agreement")
   @auth.route("/forgot_password")'''

