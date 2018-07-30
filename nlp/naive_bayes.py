# Import statements
import nltk
import random
import sys, os
proj_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, proj_dir)

from cassiopeia.models.models import db, User, Progress, Content
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy

# Custom App to load to cassiopeia_prod database, neeed utf8mb4 for emoji support
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://kruan@35.230.15.28/cassiopeia_prod?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    db.create_all()

# get_ratings()
# For each piece of content that the user has ever rated
# Tokenize the words and get the rating
# Store as a tuple in larger dictionary
def get_ratings(user_id):
    with app.app_context():
        db.init_app(app)
        db.create_all()
        ''' Grab all user's ratings from the database '''
        user_entries = Progress.query.filter_by(user_id=user_id).all()

        ''' Tokenize each piece of content's words and
            create a tuple entry [[word_list], rating] '''
        tokenized_entries = []
        for entry in user_entries:
            tokenized_words = Content.query.filter_by(id=entry.content_id).first().body.split()
            tokenized_entries.append([tokenized_words, entry.rating])
        return tokenized_entries

# clean_dict_words()
# Normalize all dict words to lower case
#def create_dict():

# find_words()
# Checks given .txt for all dict words
# Assigns true/false - denoting is_in_.txt
# def get_words():

# Define training set
# Train
# (run tests)

# Find article
# Get user skill
# Start at user skill (get all content @ given skill level)
# Run content through posterior algo
# If classified as just right, push to user
# Else skip

if __name__== "__main__":
    # Load data
    user_ratings = get_ratings(33)
    print(user_ratings)
