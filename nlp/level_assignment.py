import sys, os
proj_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, proj_dir)

from cassiopeia.models.models import db, Content, Language
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from nlp.difficulty import cal_diff
# from nlp.readability import cal_ari
# from eventregistry import *

# Custom App to load to cassiopeia_prod database, neeed utf8mb4 for emoji support
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://kruan@35.230.15.28/cassiopeia_prod?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## alternative

#with current_app.app_context()

def assign_levels():
    with app.app_context():
        db.init_app(app)
        db.create_all()


        ''' select everything from the content
        loop through it to calculate the score
        then add the it back to the database '''
        articles = Content.query.all()

        #for each article
        for article in articles:
            text = str(article.body)
            score = cal_diff(text)
            article.level = score
            # print(article.id, score)
            db.session.add(article)

        # Commit the transactions
        db.session.commit()
