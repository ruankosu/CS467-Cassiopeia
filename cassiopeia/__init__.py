import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# register bcrypt object
global_bcrypt = Bcrypt()

# create login manager for sessions
login_manager = LoginManager()

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='SuperSecret9000'
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://kruan@35.230.15.28/cassiopeia_prod?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

    # register the database commands, bcrypt and login_manager
    from cassiopeia import db
    db.init_app(app)
    login_manager.init_app(app)
    global_bcrypt.init_app(app)

    # apply the blueprints to the app
    from cassiopeia.views import auth, content, signup
    app.register_blueprint(auth.auth)
    app.register_blueprint(content.app)
    app.register_blueprint(signup.app)

    return app

