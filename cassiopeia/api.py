# Article API 
import json
from datetime import datetime
from cassiopeia.models.models import User, Content, Language, Progress
from cassiopeia import db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

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
def contents_to_obj(contents, user_info=None, languages=None, categories=None):
  payload = {}
  content_arr = []
  last_id_next = -1

  # Add user info
  if user_info is not None:
    payload['user_info'] = {
      "username" : user_info["user"].username, 
      "email" : user_info["user"].email,
      "language": user_info["language"],
      "category": user_info["category"]
    }

  payload['last_id_prev'] = list(contents)[0].id

  # Add content
  for c in contents:
    obj = {}
    obj["id"] = c.id
    obj["name"] = c.name.decode("utf-8")
    obj["language"] = str(c.language.name)
    obj["pub_date"] = datetime.strftime(c.pub_date, '%b %d, %Y')
    obj["url"] = str(c.url)
    obj["body"] = c.body.decode("utf-8")
    obj["categories"] = [str(category.name) for category in c.categories]
    obj["level"] = c.level
    content_arr.append(obj)
    payload['last_id_next'] = c.id

  # Add pagination and contents
  payload['contents'] = content_arr
  
  if len(list(contents)) < 20:
    payload['last_page'] = True
  else:
    payload['last_page'] = False

  # Add language and categories
  if languages is not None and categories is not None:
    payload['user_languages'] = languages
    payload['user_categories'] = categories

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

# Get articles with pagination, default 20 articles provided based on first language and category
# selected. There should be more work later to make it more flexible. i.e. return all Sports categories
#
# Query String:
# page - page number (int)
# language - String
# category - String
# last_id - last seen id (int)
# direction - paging direction (next, prev)
@api.route("/article", methods=['GET'])
@login_required
def getArticle():  
  try:
    db.get_db() # Establish database connection

    # Get param values
    page = request.args.get('page')
    language = request.args.get('language')
    category = request.args.get('category')
    last_id = request.args.get('last_id')
    direction = request.args.get('dir')

    # Get user 
    user_info = {}
    user = User.query.filter(User.id == current_user.id).first()

    # Get user languages and categories
    user_languages = []
    user_categories = [{"name": c.name, "selected": 0} for c in user.categories]

    # Get user level for selected language
    for l in iter(user.languages):
      selected = 0
      l_item = Language.query.filter(Language.id == l.language_id).first()
      if language is not None:
        if Language.query.filter(l_item.iso639_2 == str(language)).first():
          selected = 1
      user_languages.append({"language_name": l_item.name, "iso": l_item.iso639_2, "skill": l.skill, "selected": selected})

    # Finalize default language
    language = list(filter(lambda x: x["selected"] == 1, user_languages))
    if len(language) == 0:
      language = user_languages[0]
      language["selected"] = 1
    else:
      language = language[0]

    # Set Default category
    if category is None:
      user_categories[0]["selected"] = 1
      category = user_categories[0]

    # Set user_info
    user_info["user"] = user
    user_info["language"] = language["iso"]
    user_info["category"] = category["name"]

    # return first 20
    if int(page) == 1 and last_id is None and direction is None:
      contents = Content.query.filter(Content.language.has(Language.iso639_2 == language["iso"]), Content.level <= language["skill"]).order_by(Content.id.desc()).limit(20).all()
      return response_wrapper(contents_to_obj(contents, user_info, user_languages, user_categories), 200)
    # return next 20 based on last_id
    if direction == "next":
      contents = Content.query.filter(Content.language.has(Language.iso639_2 == language["iso"]), Content.level <= language["skill"], Content.id < last_id).order_by(Content.id.desc()).limit(20)     
    # return prev 20 based on last_id
    if direction == "prev":
      contents = Content.query.filter(Content.language.has(Language.iso639_2 == language["iso"]), Content.level <= language["skill"], Content.id > last_id).order_by(Content.id.asc()).limit(20)
      contents = list(reversed(list(contents))) # reverse before returning to client. 
    
    return response_wrapper(contents_to_obj(contents, user_info), 200)
  except Exception as ex:
    return response_wrapper({"error": str(ex)}, 500)

  return response_wrapper({"error": "Something went wrong"}, 500)

# API to handle article ratings made by the user. This will feed into the Progress table.
# The value in this table will be used for NLP and Naive Bayes learning to update the 
# user's language skill level. 
@api.route("/article/rate", methods=['POST'])
@login_required
def rateArticle():
  try:
    mysql = db.get_db() # Establish db connection

    # Get user from database
    user = User.query.filter(User.id == current_user.id).first()

    # Get data from request body
    data = json.loads(request.data)
    content_id = data["content_id"]
    rating = data["rating"]

    # Get progress object and set new data
    progress = Progress(user_id=user.id, content_id=content_id, rating=rating, read_ct=1)

    # Add to session and commit
    mysql.session.add(progress)
    mysql.session.commit()

    # Return empty object with code 200
    return response_wrapper({}, 200)

  except Exception as ex:
    return response_wrapper({"error": str(ex)}, 500)

  return response_wrapper({"error": "Something went wrong"}, 500)

# ----------------------------- Other APIs ----------------------------------- #
@api.route("/history", methods=['GET'])
@login_required
def getHistory():
  try:
    history = []
    rating_map = ["Just Right", "Too Hard", "Too Easy"]

    db.get_db()
    user = User.query.filter(User.id == current_user.id).first()
    progress = Progress.query.filter(Progress.user_id == user.id).all()

    for item in progress:
      obj = {}
      content = Content.query.filter(Content.id == item.content_id).first()
      obj["name"] = str(content.name.decode("utf-8"))
      obj["read_date"] = datetime.strftime(item.read_date,"%b %d %Y %H:%M:%S")
      obj["rating"] = rating_map[item.rating]
      history.append(obj)    

    return response_wrapper(history, 200)

  except Exception as ex:
    return response_wrapper({"error": str(ex)}, 500)

  return response_wrapper({"error": "Something went wrong"}, 500)


# ----------------------------- Request Helper  ----------------------------------- #
@api.after_request
def after_request(response):
  # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response