# Import statements
import nltk
import random
import sys, os
proj_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, proj_dir)

from cassiopeia.models.models import db, User, Progress, Content
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy

# Custom App to load to cassiopeia_prod database, need utf8mb4 for emoji support
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://kruan@35.230.15.28/cassiopeia_prod?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# get_ratings()
''' Gets all Progress entries for the given user (by id)
    and tokenizes the words for each entry's content. Stores
    tokenized word list and user-assigned rating in container
    called tokenized_entries as a tuple for each piece of
    user-rated content '''
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
            tokenized_words_b = Content.query.filter_by(id=entry.content_id).first().body.split()
            tokenized_words = []
            ''' Decode from binary to utf8 '''
            for word in tokenized_words_b:
                tokenized_words.append(word.decode('utf8'))
            tokenized_entries.append([tokenized_words, entry.rating])
        return tokenized_entries



# get_words()
''' Grabs all words from all user-rated entries and
    normalizes each word to lowercase. Appends each word
    to a list called all_words '''
def get_words(entries):
    with app.app_context():
        db.init_app(app)
        db.create_all()

        # Container for all words
        all_words = []

        ''' For each entry in the list of entry tuples
                For each word in tuple[0]
                    Append that word to all_words list '''
        for entry in entries:
            for word in entry[0]:
                all_words.append(word.lower())

        return all_words


# find_words()
# Checks given .txt for all dict words
# Assigns true/false - denoting is_in_.txt
def find_words(content_id, feature_words):
    with app.app_context():
        db.init_app(app)
        db.create_all()

        # Create a set of words from the given content
        words = set(Content.query.filter_by(id=content_id).first().body.decode('utf8'))
        features = {}
        for word in feature_words:
            features[word] = (word in words)
        return features


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
    #print(user_ratings)
    all_words = get_words(user_ratings)
    #print(all_words)
    # Convert all_words to dictionary with word frequency denoted
    all_words = nltk.FreqDist(all_words)
    # Create a list of 3000 most frequent words
    feature_words = list(all_words.keys())[:3000]
    # Call find_words on a document
    '''word_match = find_words(90, feature_words)
    for word in word_match:
        if word_match[word] == True:
            print(word)'''


