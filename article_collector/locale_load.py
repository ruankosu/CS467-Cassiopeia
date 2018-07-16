import os
import json
import sys
proj_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, proj_dir)

from cassiopeia.models.models import db, Country, Language
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Custom App to load to cassiopeia_prod database, neeed utf8mb4 for emoji support
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://kruan@35.230.15.28/cassiopeia_prod?charset=utf8mb4'

f = open('all.json', 'r') # From https://restcountries.eu/#api-endpoints-language
buf = f.read()
obj_dict = json.loads(buf)

with app.app_context():
  db.init_app(app)
  db.create_all()

  language_hash = set()
  for c in obj_dict:
    country = Country(name=c['name'], alpha2code=c['alpha2Code'], alpha3code=c['alpha3Code'], flag_image=c['flag'])

    for l in c['languages']:
      new_language = Language.query.filter(Language.name==l['name']).first()
      if new_language is None:
        new_language = Language(name=l['name'], iso639_1=l['iso639_1'], iso639_2=l['iso639_2'])
        db.session.add(new_language)      
              
      country.languages.append(new_language)

    db.session.add(country)
  
  db.session.commit()
