# Article API 
from cassiopeia.models.models import User, Content, Language
from cassiopeia import db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, json
)
from flask_cors import CORS

# Helps handle user sessions
from flask_login import login_user, current_user, logout_user, login_required

api = Blueprint('api', __name__, url_prefix='/api')

# Flask response wrapper
def response_wrapper(data, status): 
  response = current_app.response_class(
    response=json.dumps(data),
    status=status,
    mimetype='application/json'
  )
  return response

# Convert contents to Python dictionary
def contents_to_obj(contents):
  payload = {}
  content_arr = []
  last_id = -1

  for c in contents:
    obj = {}
    obj["id"] = c.id
    obj["name"] = str(c.name)
    obj["language"] = str(c.language.name)
    obj["pub_date"] = str(c.pub_date)
    obj["url"] = str(c.url)
    obj["categories"] = [str(category.name) for category in c.categories]
    obj["level"] = c.level
    content_arr.append(obj)
    last_id = c.id

  payload['last_id'] = last_id
  payload['contents'] = content_arr
  return payload

# ----------------------------- Article APIs ----------------------------------- #
# Get total number of pages for all articles, limit 20 articles per page
@api.route("/articles/pages", methods=['GET'])
def getArticlePages():
  if current_user.is_authenticated: 
    mysql = db.get_db()
    rows = mysql.session.query(Content).count()
    if rows:
      data = { "total_article_count" :  rows}
      return response_wrapper(data, 200)
  return response_wrapper({"error": "Something went wrong"}, 500)

# Get articles with pagination 
# Query String:
# page - page number (int)
# last_id - last seen id (int)
# direction - paging direction (next, prev)
@api.route("/article", methods=['GET'])
@login_required
def getArticle():  
  try:
    mysql = db.get_db() # Establish database connection
    page = request.args.get('page')
    language = request.args.get('language')
    last_id = request.args.get('last_id')
    direction = request.args.get('dir')
    skill = None

    # Get user level for selected language
    user = User.query.filter(User.id == current_user.id).first()
    for l in user.languages:
      selected_lang = Language.query.filter(Language.iso639_2 == str(language)).first()
      if selected_lang is not None:
        skill = l.skill

    # return first 20
    if int(page) == 1 and last_id is None and direction is None:
      contents = Content.query.filter(Content.language.has(Language.iso639_2 == language), Content.level <= skill).limit(20).all()
      return response_wrapper(contents_to_obj(contents), 200)

    # return next 20 based on last_id
    if direction == "next":
      contents = Content.query.filter(Content.language.has(Language.iso639_2 == language), Content.level <= skill, Content.id > last_id).order_by(Content.id.asc()).limit(20)
      
    # return prev 20 based on last_id
    if direction == "prev":
      contents = Content.query.filter(Content.language.has(Language.iso639_2 == language), Content.level <= skill, Content.id < last_id).order_by(Content.id.asc()).limit(20)
    
    return response_wrapper(contents_to_obj(contents), 200)
  except Exception as ex:
    return response_wrapper({"error": str(ex)}, 500)

  return response_wrapper({"error": "Something went wrong"}, 500)
 
# ----------------------------- Other APIs ----------------------------------- #



    






