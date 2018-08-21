import sys, os, pickle
import codecs
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)
proj_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, proj_dir)

from cassiopeia.models.models import db, Content, UserLangSkill, UserSortedContent, User
from flask import Flask, current_app, g
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from nlp.naive_bayes import get_classifier, get_feature_set, classify


# Custom App to load to cassiopeia_prod database, neeed utf8mb4 for emoji support
app = Flask(__name__)
# app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://kruan@35.230.15.28/cassiopeia_prod?charset=utf8mb4'


def refresh_content_level(current_user_id):
    with app.app_context():
        db.init_app(app)
        db.create_all()

        #only curate for the last 50 articles
        content_text = Content.query.order_by(Content.id.desc()).limit(50).all()

        # pickled_classifier = User.query.filter_by(id=current_user_id).first().classifier
        # g.classifier = pickle.loads(pickled_classifier)

        # pickled_feature_set = User.query.filter_by(id=current_user_id).first().feature_set
        # g.feature_set = pickle.loads(pickled_feature_set)
        classifier = get_classifier(current_user_id)
        feature_set = get_feature_set(current_user_id)

        # classify and create as a new entry
        for content_item in content_text:
            result = classify(content_item.body, classifier, feature_set)
            print(result)
            # only the suitable entries are added
            if result == 0 or result == 1:
                article_entry = UserSortedContent(user_id=current_user_id, content_id=content_item.id, sortedSkill=result)
                db.session.add(article_entry)
        # commit the change
        db.session.commit()

def refresh_user_level(current_user_id):
    with app.app_context():
        db.init_app(app)
        db.create_all()

        # get all articles in the curated table for this user
        user_curated_article_levels = UserSortedContent.query.filter_by(user_id=current_user_id).all()

        # calculate standard deviaion of the user level
        sqd_deviations = 0
        for entry in user_curated_article_levels:
            level = (Content.query.filter_by(id=entry.content_id).first()).level
            sqd_deviations += level ** 2
        if len(user_curated_article_levels) > 0:
            std_deviation = (sqd_deviations / len(user_curated_article_levels)) ** 0.5
        else:
            std_deviation = 0

        # add user skill to the user_lang_skill table
        user = UserLangSkill.query.filter_by(user_id=current_user_id).first()
        if std_deviation > 0:
            # user = UserLangSkill(user_id=current_user_id, language_id=815, skill=std_deviation)
            user.skill = std_deviation
            db.session.add(user)
            db.session.commit()

        #     else:
        #     user.skill = std_deviation
        # db.session.add(user)
        # db.session.commit()
        #
        # for level in user_curated_article_levels:
        #     sqd_deviations += level[0] ** 2
        # std_deviation = (sqd_deviations / len(user_curated_article_levels)) ** 0.5
        #articles = User.query.


if __name__== "__main__":
    refresh_content_level(28)
