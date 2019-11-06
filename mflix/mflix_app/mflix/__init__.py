from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mflix-app-mongodb'
# Override the configuration values from the configuration file, which is
# pointed by "MFLIX_SETTINGS" environment variable
app.config.from_envvar('MFLIX_SETTINGS', silent=True)

# Initialize the LoginManager object with the newly create application
login_manager = LoginManager(app)

from .auth import *
from .mflix import *

# Why not using "Application Factory Pattern"?
# Because if we use a application factory, when registering the routes, they
# won't have access to the the actual application object itself to be registered
# on, so we have to use blueprints, which I don't want to use since this is
# meant to be a very simple, introductory application.
