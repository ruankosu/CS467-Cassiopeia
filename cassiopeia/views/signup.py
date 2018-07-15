import functools
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from cassiopeia.db import get_db

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, "cassiopeia")
template_dir = os.path.join(template_dir, "templates")

app = Blueprint('signup', __name__, template_folder=template_dir)

languages = [
	{
        'name': 'English',
		'flag': 'britain.png',
	},
	{
        'name': 'Chinese',
		'flag': 'china.png',
	},
	{
		'name': 'German',
		'flag': 'germany.png',
	}
]

@app.route('/register')
def register():
    return render_template('signup/signup.html')


@app.route('/register/language')
def language():
    return render_template('signup/language.html', langs=languages)

@app.route('/register/skill')
def skill():
    return render_template('signup/skill.html')

categories = [
	{
        'name': 'Sports',
		'icon': 'sports.png',
	},
	{
        'name': 'Politics',
		'icon': 'politics.png',
	},
	{
		'name': 'Kids/Family',
		'icon': 'kids_family.png',
	},	
    {
		'name': 'Finance',
		'icon': 'finance.png',
	},	
    {
		'name': 'Health',
		'icon': 'health.png',
	},	{
		'name': 'Education',
		'icon': 'education.png',
	}
]
    
@app.route('/register/interests')
def interests():
    return render_template('signup/interests.html', categories=categories)

