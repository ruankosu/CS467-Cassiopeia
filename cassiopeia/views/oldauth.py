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
    '''if current_user.is_authenticated:
        return redirect(url_for('home.home'))'''
    if request.method == 'POST':
        flash('Test flash.', 'error')
        # Confirm username is unique
        username = request.form['username']
        already_taken = User.query.filter_by(username=username).first()
        if already_taken:
            flash('Username already in use. Please choose a different one.', 'error')
            #reload form
            #return render_template('signup/signup.html', title='Sign Up')

        # Confirm email is unique
        email = request.form['inputEmail']
        email_in_use = User.query.filter_by(email=email).first()
        if email_in_use:
            flash('Email already associated with an account. Please log in or use a different email address.', 'error')
            #return redirect(url_for('signup'))

        # Confirm registration password matches confirmation password
        # If password != confirmation password, flash error
        password = request.form['inputPassword']
        if password != request.form['confirmPassword']:
            flash('Passwords entered do not match. Please correct and resubmit.', 'error')
            # redirect to signup form
            #return redirect(url_for('signup'))

        else:
            hashed_pwd = global_bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, email=email, password=password)
            mysql.session.add(new_user)
            mysql.session.commit()
            #flash('Account created! Please set your preferences.', 'success')
            return redirect(url_for('signup.language'))

    return render_template('signup/signup.html', title='Sign Up', form=form)



@auth.route("/login", methods=['GET', 'POST'])
def login():
    '''if current_user.is_authenticated:
        return redirect(url_for('home.home'))'''

    if post_method == 'POST':
        # Check email is in db. If not, flash message and ask to re-enter
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            # Get password for user given email. Check password is same.
            password_entered = request.form['password']
            user_password = user.password
            #if bcrypt.check_password_hash(user.password, password_entered):
                #login_user(user)
                # Flash success message
                #flash('Login successful.', 'success')


            # Redirect to home
            return redirect(url_for('home.home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Log In')


@auth.route("/logout")
def logout():
    logout_user()
    return
    #return redirect(url_for(''))


'''@auth.route("/user_agreement")
   @auth.route("/forgot_password")'''

