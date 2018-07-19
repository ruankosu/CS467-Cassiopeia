import functools
import os
import sys
from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
#from cassiopeia.models.models import db
from cassiopeia.models.models import User
from cassiopeia import db, global_bcrypt
from cassiopeia.views.signup_forms import (RegistrationForm, LoginForm)

# Helps handle user sessions
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth', __name__)


# Routes
@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    mysql = db.get_db()
    flash('Attempt FLash!', 'success')
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('signup.language'))
    return render_template('signup/signup.html', title='Sign Up', form=form)



'''@auth.route("/login", methods=['GET', 'POST'])
def login():
            return redirect(url_for('home.home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Log In')


@auth.route("/logout")
def logout():
    logout_user()
    return
    #return redirect(url_for(''))


@auth.route("/user_agreement")
   @auth.route("/forgot_password")'''

