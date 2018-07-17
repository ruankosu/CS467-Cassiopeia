import functools
import os
from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from cassiopeia.models.models import User
from cassiopeia import db

# Register database context
db.get_db()

# Helps handle user sessions
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth', __name__)


# Routes
@auth.route("/register", method=['POST'])
def register():
    # Confirm username is unique
    username = User.query.filter_by(request.form('username')).first()
    if username:
        flash('Username already in use. Please choose a different one.', 'error')
        #return redirect(url_for(''))

    # Confirm email is unique
    username = User.query.filter_by(request.form('inputEmail')).first()
    if username:
        flash('Email already associated with an account. Please log in or use a different email address.', 'error')
        #return redirect(url_for(''))

    # Confirm registration password matches confirmation password
    # If password != confirmation password, flash error
    password = request.form('inputPassword')
    if password != request.form('confirmPassword'):
        flash('Passwords entered do not match. Please correct and resubmit.', 'error')

    ''' If form is validated after being submitted,
        Create new user with given form data
        add and commit user
        flash message account creation successful
        return to login page
    return the rendered template for registration'''


@auth.route("/login", method=['GET', 'POST'])
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


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for(''))


'''@auth.route("/user_agreement")
   @auth.route("/forgot_password")'''

