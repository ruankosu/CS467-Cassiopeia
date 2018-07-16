import sys, os
proj_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, proj_dir)

from cassiopeia.models.models import db, Content, Language
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from eventregistry import *

# Custom App to load to cassiopeia_prod database, neeed utf8mb4 for emoji support
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://kruan@35.230.15.28/cassiopeia_prod?charset=utf8mb4'

with app.app_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()

    # Add English Language
    language = Language(name="English")
    db.session.add(language)
    db.session.commit() # Insert into Language table for FK rquirement

    # Query Event Registry
    er = EventRegistry(apiKey = "0592c16f-ac74-4f47-9443-e055a21b61dd")
    q = QueryArticlesIter.initWithComplexQuery("{\"$query\":{\"$and\":[{\"categoryUri\":{\"$and\":[\"dmoz/Sports\",\"dmoz/Sports/Soccer\"]}},{\"dateStart\":\"2018-01-01\",\"dateEnd\":\"2018-07-13\",\"lang\":\"eng\"}]}}")
    
    # Grab 10 pages of results with 100 articles each
    for i in range(1,11):
        q.setRequestedResult(RequestArticlesInfo(page = i, count = 100,
            returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(concepts = True, categories = True, image = True))))
        res = er.execQuery(q)

        # Load to Content table
        # '<name=%r, pub_date=%r, url=%r, body=%r, level=%r>
        for article in res['articles']['results']:
            body_str = bytes(article['body'], 'utf-8').decode('utf-8','ignore')
            content = Content(name=article['title'], language_id=1, pub_date=article['date'], url=article['url'], body=body_str, level=-1.0)
            db.session.add(content) 

    # Commit the transactions
    db.session.commit()

