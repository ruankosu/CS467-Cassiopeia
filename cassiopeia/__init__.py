import os
from flask import Flask
#from cassiopeia.config import Config

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    #app.config.from_object(Config)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='SuperSecret9000',
        # store the database in the instance folder
        SQLALCHEMY_DATABASE_URI=os.path.join(app.instance_path, 'sqlite:///site_test.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # @app.route('/')
    # def hello():
    #     return 'Hello, World!'

    # register the database commands
    from cassiopeia.models.models import db
    with app.app_context():
        db.init_app(app)

    # apply the blueprints to the app
    from cassiopeia.views import auth, content
    app.register_blueprint(auth.bp)
    app.register_blueprint(content.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule('/', endpoint='index')

    return app
