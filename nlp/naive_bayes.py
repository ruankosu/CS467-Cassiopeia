'''
    Title: naive_bayes.py
    Description: Rudimentary implentation of the NLTK's Naive
        Bayes classifier for text classification.
    Author: Kendra Ellis, copyright 2018
    For: CS467 Cassiopeia - NLP1 Group Project
    Notes: This code is highly informed/influenced by the set of
        tutorials found here:
        https://pythonprogramming.net/text-classification-nltk-tutorial/

        Additionally, instructions found here were particularly helpful:
            https://www.nltk.org/book/ch06.html
'''


# Import statements
import nltk
import sys, os, pickle
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
''' Checks body of given content for all dict words
    Assigns true/false - denoting word is in content for
    a given word list '''
def find_words(word_list, feature_words):
    # Create a set of words from the given content
    words = set(word_list)
    features = {}
    for word in feature_words:
        features[word] = (word in words)
    return features


# find_words_doc()
''' Checks given content for all dict words
    Assigns true/false - denoting word is in content for
    a given piece of content (by id) '''
def find_words_doc(content_id, feature_words):
    with app.app_context():
        db.init_app(app)
        db.create_all()

        # Create a set of words from the given content
        words = set(Content.query.filter_by(id=content_id).first().body.decode('utf8'))
        features = {}
        for word in feature_words:
            features[word] = (word in words)
        return features


# create_featuresets()
''' Creates and returns a list of tuples where the first entry
    is a find_words() list for a given article, and the second
    is the article's category for ALL articles in list
    returned by get_ratings() '''
def create_featuresets(feature_words, user_ratings):
    return [(find_words(article, feature_words), category) for (article, category) in user_ratings]


# create_classifier()
''' Creates and stores a pickled classifier (and feature set, i.e., words to use
    for classification) for the given user.
    Parameters:
        user_id - db id of user for whom the classifier will be created
        word_ct - max number of words to use when creating most frequent
            word list '''
def create_classifier(user_id, word_ct):
    # Load data
    user_ratings = get_ratings(user_id)

    #print(user_ratings)
    all_words = get_words(user_ratings)

    # Convert all_words to dictionary with word frequency denoted
    all_words = nltk.FreqDist(all_words)

    # Create a list of n most frequent words where n = word_ct
    feature_words = list(all_words.keys())[:word_ct]

    # Create featuresets
    featuresets = create_featuresets(feature_words, user_ratings)

    # Define training and testing sets by
    # splitting set of all reviews in half
    # training_set = featuresets[:feature_ct]
    # testing_set = featuresets[feature_ct:]

    # Train Naive-Bayes Algorithm
    classifier = nltk.NaiveBayesClassifier.train(featuresets)

    # Show accuracy and 15 most informative features
    # print("Naive Bayes Algo accuracy percent: ", (nltk.classify.accuracy(classifier, testing_set)) * 100)
    # classifier.show_most_informative_features(15)

    # Pickle the dictionary for later use
    saved_dictionary = pickle.dumps(feature_words)

    # Pickle classifier for later use
    saved_classifier = pickle.dumps(classifier)

    # Save dictionary and classifier in user's row in DB
    with app.app_context():
        db.init_app(app)
        db.create_all()

        # Get user
        user = User.query.filter_by(id=user_id).first()
        user.feature_set = saved_dictionary
        user.classifier = saved_classifier
        # Commit updates
        db.session.commit()

    #return [classifier, feature_words]
    return


# classify()
''' Returns the predicted category (-1, 0, 1)
    and takes the text to classify
    and the user's id as arguments '''
def classify(text, user_id):

    # Retrieve classifier from db
    with app.app_context():
        db.init_app(app)
        db.create_all()
        pickled_classifier = User.query.filter_by(id=user_id).first().classifier
        classifier = pickle.loads(pickled_classifier)
        # Retrieve dictionary from db
        pickled_feature_set = User.query.filter_by(id=user_id).first().feature_set
        feature_set = pickle.loads(pickled_feature_set)

        # Featurize the text to classify
        featurized_text = find_words(text, feature_set)

        # Feed featurized text to classifier
        # Return predicted category
        return classifier.classify(featurized_text)


'''if __name__== "__main__":
    #TEST

    #Create classifier and featureset for user #39, test_nb_user
    create_classifier(39, 5000)
    #Get a text from the database
    with app.app_context():
        db.init_app(app)
        db.create_all()
        test_text = Content.query.filter_by(id=1).first().body
    #Classify a text and return the predicted category
    print(classify(test_text, 39))'''
