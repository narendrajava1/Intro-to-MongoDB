import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_restful import Api
from pymongo import MongoClient

user = os.environ['USER']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']
MFLIX_DB_URI = f"mongodb+srv://{user}:{password}@cluster0-hanbs.mongodb.net/{db_name}?retryWrites=true&w=majority"

try:
    db = MongoClient(MFLIX_DB_URI)[db_name]
except KeyError:
    raise Exception("You haven't configured your MFLIX_DB_URI!")

ma = Marshmallow()
bcrypt = Bcrypt()

from .resources.auth import UserAuth, UserList

app = Flask(__name__)
app.config['SECRET_KEY'] = 'auth-service-mongodb'

api = Api(app)
api.add_resource(UserList, '/users')
api.add_resource(UserAuth, '/user-auth')

ma.init_app(app)
bcrypt.init_app(app)
