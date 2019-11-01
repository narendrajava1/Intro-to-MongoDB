import os

from flask import Flask
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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'movie-service-mongodb'

ma = Marshmallow(app)

api = Api(app)

from .resources.comment import MovieComment, MovieComments
from .resources.movie import MovieGenreList, MovieItem, MovieList

api.add_resource(MovieList, '/movies')
api.add_resource(MovieItem, '/movie/<id>')
api.add_resource(MovieComments, '/movie/<id>/comments')
api.add_resource(MovieComment, '/movie/<movie_id>/comments/<comment_id>')
api.add_resource(MovieGenreList, '/movie-genres')


# if __name__ == '__main__':
#     app.run('0.0.0.0', 8000, debug=True)
