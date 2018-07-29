# Functions to create/delete 1000 test_user progress entries
# in the database for testing Naive Bayes implementation
import sys, os
proj_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, proj_dir)

from cassiopeia.models.models import db, Content, Progress, User
from cassiopeia import global_bcrypt
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy

# Custom App to load to cassiopeia_prod database, neeed utf8mb4 for emoji support
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://kruan@35.230.15.28/cassiopeia_prod?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define rating upper thresholds
EASY = 5
JUST_RIGHT = 9
# Sets number of Progress entries created/deleted
ARTICLE_CT = 3

def create_entries():
    with app.app_context():
        db.init_app(app)
        db.create_all()

        # Create test user
        #password = global_bcrypt.generate_password_hash('password').decode('utf-8')
        #user = User(username='test_nb_user', email='testnb@test.com', password=password)
        #db.session.add(user)
        #db.session.commit()
        # Get new user's id
        user = User.query.filter_by(username='test_nb_user').first()
        user_id = user.id


        ''' select everything from the content '''
        articles = Content.query.all()

        ''' Create 500 progress entries for the test user from the
            first 500 entries in the Content table. Rating -1 == too easy,
            0 == just right, 1 == too difficult '''
        for i in range(ARTICLE_CT):
            content = articles[i]
            score = content.level
            # Add appropriate Progress entry
            if score >= 0 and score < EASY:
                entry = Progress(user_id=user_id, content_id=content.id, rating=-1, read_ct=1)
                db.session.add(entry)
            elif score >= 5 and score < JUST_RIGHT:
                entry = Progress(user_id=user_id, content_id=content.id, rating=0, read_ct=1)
                db.session.add(entry)
            else:
                entry = Progress(user_id=user_id, content_id=content.id, rating=1, read_ct=1)
                db.session.add(entry)
        # Update DB
        db.session.commit()


def delete_entries():
    with app.app_context():
        db.init_app(app)
        db.create_all()
        user = User.query.filter_by(username='test_nb_user').first()
        if user:
            user_id = user.id
        # Query DB for user Progress entries. While true, delete.
        entry = Progress.query.filter_by(user_id=user_id).first()
        while entry:
            db.session.delete(entry)
            entry = Progress.query.filter_by(user_id=user_id).first()
        db.session.delete(user)
        db.session.commit()


if __name__== "__main__":
    create_entries()
    #delete_entries()

