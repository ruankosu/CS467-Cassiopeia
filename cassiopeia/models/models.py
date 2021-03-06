from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, current_app
from cassiopeia import login_manager
from flask_login import UserMixin

# Create database object
db = SQLAlchemy()

# Decorater that gets user from user id
@login_manager.user_loader
def load_user(user_id):
    with current_app.app_context():
        db.init_app(current_app)
        return User.query.get(int(user_id))

# User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    # We should create a function for password hashing
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    native_language = db.Column(db.Integer, db.ForeignKey('language.id'), nullable=True)
    feature_set = db.Column(db.PickleType, nullable=True)
    classifier = db.Column(db.PickleType, nullable=True)
    languages = db.relationship('UserLangSkill', backref='user')
    # Allows us to get all pieces of content associate with a user on the user_sorted_content table
    sorted_content = db.relationship('UserSortedContent', backref='user', lazy=True)
    # Allows us to get all Progress entries assoc. with a given user
    progress = db.relationship('Progress', backref='user', lazy=True)
    sorted_content = db.relationship('UserSortedContent', backref='user', lazy=True)
    def __repr__(self):
        return '<username=%r, first_name=%r, last_name=%r, email=%r>' % (self.username, self.email)


# Country
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    alpha2code = db.Column(db.String(2), unique=True, nullable=False)
    alpha3code = db.Column(db.String(3), unique=True, nullable=False)
    # Need to set default flag image
    flag_image = db.Column(db.String(255), nullable=False, default='default.jpg')

    def __repr__(self):
        return '<name=%r, alpha2code=%r, alpha3code=%r, flag_image=%r>' % (self.name, self.alpha2code, self.alpha3code, self.flag_image)


# Category
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    icon_img = db.Column(db.String(60), nullable=True)
    users = db.relationship('User', secondary='user_category', backref='categories', lazy='dynamic')
    articles = db.relationship('Content', secondary='content_category', backref='categories', lazy='dynamic')

    def __repr(self):
        return '<name=%r, icon_img=%r>' % (self.name, self.icon_img)


# Language
class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    iso639_1 = db.Column(db.String(2), unique=True, nullable=False)
    iso639_2 = db.Column(db.String(3), unique=True, nullable=False)
    # Allows us to get all country items for the given language as indicated on the locale table
    countries = db.relationship('Country', secondary='locale', backref='languages', lazy='dynamic')
    # This relationship backref may not be used in practice, allows
    # us to get all users whose native language matches the lang in question
    users = db.relationship('UserLangSkill', backref='language', lazy=True)
    # Allows us to get all content items in the given language
    content = db.relationship('Content', backref='language', lazy=True)

    def __repr__(self):
        return '<name=%r iso639_1=%r, iso639_2=%r>' % (self.name, self.iso639_1, self.iso639_2)


# Locale table (many-to-many relationship for language and country)
locale = db.Table('locale',
    db.Column('language_code', db.String(3), db.ForeignKey('language.iso639_2'), nullable=False),
    db.Column('country_code', db.String(3), db.ForeignKey('country.alpha3code'), nullable=False)
)

class UserSortedContent(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), primary_key=True, nullable=False)
    sortedSkill = db.Column(db.Integer, default=0, nullable=False)
# User sorted content (many-to-many relationship for user and content)


class UserLangSkill(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'), primary_key=True, nullable=False)
    skill = db.Column(db.Float, default=0, nullable=False)
    # language = db.relationship('Language', backref='users')
    # user = db.relationship('User', backref='languages')

# # User_Lang_Skill table (many-to-many for user and foreign language)
# user_lang_skill = db.Table('user_lang_skill',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
#     db.Column('language_id', db.Integer, db.ForeignKey('language.id'), nullable=False),
#     db.Column('skill', db.Float, default=0, nullable=False)
# )

# User_categories table (many-to-many for user and interest categories)
user_category = db.Table('user_category',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False),
)

# Content
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    # one-to-many language to content
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(2083), nullable=False)
    body = db.Column(db.Text, nullable=False)
    level = db.Column(db.Float, nullable=False)
    # Allows us to get all pieces of content associate with a user on the user_sorted_content table
    sorted_content_user = db.relationship('UserSortedContent', backref='content', lazy=True)

    # Allows us to get all progress objects related to a given piece of content
    # May not be used in our app at all
    progress = db.relationship('Progress', backref='content', lazy=True)

    def __repr(self):
        return '<name=%r, pub_date=%r, url=%r, body=%r, level=%r>' % (self.name, self.pub_date, self.url, self.body, self.level)


# Content_Category table (many-to-many relationship for content/category)
content_category = db.Table('content_category',
    db.Column('content_id', db.Integer, db.ForeignKey('content.id'), primary_key=True, nullable=False),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True, nullable=False)
)


# Progress
class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    read_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=False)
    read_ct = db.Column(db.Integer, nullable=False)

    def __repr(self):
        return '<read_date=%r, rating=%r, read_ct=%r>' % (self.read_date, self.rating, self.read_ct)
