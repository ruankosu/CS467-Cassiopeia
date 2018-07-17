import functools
import os
from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_bcrypt import Bcrypt
# Helps handle user sessions
from flask_login import login_user, current_user, logout_user, login_required

'''template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, "cassiopeia")
template_dir = os.path.join(template_dir, "templates")'''

auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder=template_dir)
bcrypt = Bcrypt()

@auth.route("/register", method=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

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
    return redirect(url_for('main.home'))


'''@auth.route("/user_agreement")
   @auth.route("/forgot_password")

