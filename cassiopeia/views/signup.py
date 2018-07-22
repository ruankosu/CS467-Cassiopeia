import functools
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from cassiopeia import db
from cassiopeia.models.models import Language, Country, Category, User, UserLangSkill


template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, "cassiopeia")
template_dir = os.path.join(template_dir, "templates")

app = Blueprint('signup', __name__, template_folder=template_dir)

@app.route('/register')
def register():
    return render_template('signup/signup.html')

@app.route('/register/language', methods=['GET', 'POST'])
@app.route('/register/<user_id>/language', methods=['GET', 'POST'])
def language(user_id):
	mysql = db.get_db()
	if user_id is not None:
		lang = request.form.get('lang')
		if lang is not None:
			language = Language.query.filter(Language.name == lang).first()
			return redirect(url_for('signup.skill', user_id=user_id, lang_id=language.id))

	# For now, we'll just defaul to Chinese, English, and German. We'll need to update this route if we want to support all languages
	default_countries = Country.query.filter((Country.alpha3code=='CHN') | (Country.alpha3code=='GBR') | (Country.alpha3code=='DEU')).all()
	languages = [{'name': c.languages[0].name, 'flag': c.flag_image} for c in default_countries]
	return render_template('signup/language.html', langs=languages)

@app.route('/register/skill', methods=['GET', 'POST'])
@app.route('/register/<user_id>/skill/<lang_id>', methods=['GET', 'POST'])
def skill(user_id, lang_id):
	mysql = db.get_db()
	if user_id is not None and lang_id is not None:
		skill = request.form.get('skill')
		if skill is not None:
			language = Language.query.filter(Language.id==lang_id).first()
			user = User.query.filter(User.id==user_id).first()
			uls = UserLangSkill(user_id=user.id, language_id=language.id, skill=skill)
			mysql.session.add(uls)
			mysql.session.commit()
			return redirect(url_for('signup.interests', user_id=user_id))
	return render_template('signup/skill.html')

@app.route('/register/<user_id>/interests', methods=['GET', 'POST'])
def interests(user_id):
	mysql = db.get_db()
	if user_id is not None:
		interests = request.form.getlist('categories')
		if len(interests) > 0:
			for name in interests:
				category = Category.query.filter(Category.name == name).first()
				user = User.query.filter(User.id == user_id).first()
				user.categories.append(category)
				mysql.session.add(user)
			# Commit to db
			mysql.session.commit()
			return redirect(url_for("content.index"))

	results = Category.query.all()
	categories = [{'name': r.name, 'icon': r.icon_img} for r in results]
	return render_template('signup/interests.html', categories=categories)

