import functools
import os
import sys
from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
#from cassiopeia.models.models import db
from cassiopeia.models.models import User
#from cassiopeia import bcrypt
from cassiopeia import db

# Helps handle user sessions
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth', __name__)


# Routes
@auth.route("/register", methods=['GET', 'POST'])
def register():
    mysql = db.get_db()
    if request.method == 'POST':
        '''# Confirm username is unique
        username = request.form['username']
        already_taken = User.query.filter_by(username=username).first()
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
        password = request.form['inputPassword']
        if password != request.form['confirmPassword']:
            flash('Passwords entered do not match. Please correct and resubmit.', 'error')
            # redirect?'''
        email = request.form['inputEmail']
        username = request.form['username']
        password = request.form['inputPassword']
        print(email+' '+username+' '+password, file=sys.stderr)
        #hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=password)
        mysql.session.add(new_user)
        mysql.session.commit()
        print("Committed to db successfully", file=sys.stderr)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup/signup.html', title='Sign Up')



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

