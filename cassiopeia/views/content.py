import os
from flask import (
            Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from flask_login import login_user, current_user, logout_user, login_required

from cassiopeia.views.auth import login_required
from cassiopeia import db
from cassiopeia.models.models import Content, User, Language

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, "cassiopeia")
template_dir = os.path.join(template_dir, "templates")

app = Blueprint('content', __name__, template_folder=template_dir)

# Clear or modify all routes below
@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        payload = {}
        user = User.query.filter(User.username == current_user.username).first()
        payload["username"] = user.username
        payload["categories"] = []
        payload["languages"] = []
        payload["history"] = []
        for c in user.categories:
            payload["categories"].append(c.name)
        
        for l in user.languages:
            language = Language.query.filter(Language.id == l.language_id).first()
            payload["languages"].append(language.name)
        
        return render_template("content/main.html", payload=payload)
    return render_template("home/home.html")

@app.route('/about', methods=['GET'])
def about():
    return render_template("home/about.html")

@app.route('/tandc', methods=['GET'])
def tandc():
    return render_template("home/t&c.html")

# @app.route('/login', methods=('GET', 'POST'))
# @login_required
# def create():
#     """Create a new post for the current user."""
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'INSERT INTO post (title, body, author_id)'
#                 ' VALUES (?, ?, ?)',
#                 (title, body, g.user['id'])
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/create.html')


# @app.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
# def update(id):
#     """Update a post if the current user is the author."""
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ? WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/update.html', post=post)


# @app.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
#     """Delete a post.
#     Ensures that the post exists and that the logged in user is the
#     author of the post.
#     """
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('blog.index'))
