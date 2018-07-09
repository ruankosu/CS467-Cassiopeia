from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    # We should create a function for password hashing
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    native_language = db.Columng(db.Integer, db.ForeignKey('language.id', nullable=False)
    # Allows us to get all Progress entries assoc. with a given user
    progress = db.relationship('Progress', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.first_name}', '{self.last_name}', '{self.email}')"


# Country
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    # Need to set default flag image
    flag_image = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Country('{self.name}', '{self.flag_image}')"


# Category
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)

    def __repr(self):
        return f"Category('{self.name}')"


# Language
class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    # This relationship backref may not be used in practice, allows
    # us to get all users whose native language matches the lang in question
    users = db.relationship('User', backref='language', lazy=True)
    # Allows us to get all content items in the given language
    content = db.relationship('Content', backref='language', lazy=True)

    def __repr(self):
        return f"Language('{self.name}')"


# Locale table (many-to-many relationship for language and country)
locale = db.Table('locale',
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'), primary_key=True, nullable=False),
    db.Column('country_id', db.Integer, db.ForeignKey('country.id'), primary_key=True, nullable=False)
)

# User_Lang_Skill table (many-to-many for user and foreign language)
user_lang_skill = db.Table('user_lang_skill',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'), nullable=False),
    db.Column('skill', db.Float, nullable=False)
)


# Content
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    # one-to-many language to content
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(2083), nullable=False)
    level = db.Column(db.Float, nullable=False)
    # Allows us to get all progress objects related to a given piece of content
    # May not be used in our app at all
    progress = db.relationship('Progress', backref='content', lazy=True)

    def __repr(self):
        return f"Content('{self.name}', '{self.pub_date}', '{self.url}', '{self.level}')"


# Content_Category table (many-to-many relationship for content/category)
content_category = db.Table('content_category',
    db.Column('content_id', db.Integer, db.ForeignKey('content.id'), primary_key=True, nullable=False,
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True, nullable=False)
)


# Progress
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    read_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=False)
    read_ct = db.Column(db.Integer, nullable=False)

    def __repr(self):
        return f"Progress('{self.read_date}', '{self.rating}', '{self.read_ct}')"
