# -*- coding: utf-8 -*-

"""
Interface module with MongoDB.
"""

import os
from typing import Tuple

from bson.errors import InvalidId
from pymongo import MongoClient

try:
    db = MongoClient(os.environ['MFLIX_DB_URI']).mflix
except KeyError:
    raise Exception("You haven't configured your MFLIX_DB_URI!")


def get_movies(filters: dict, page: int,
               movies_per_page: int) -> Tuple[list, int]:
    """
    Returns a movie list on the given page based on the given filters and number
    of movies per page.
    :param filters: dict
    :param page: int
    :param movies_per_page: int
    :return: tuple
    """
    sort_key = 'tomatoes.viewers.numReviews'

    if '$text' in filters:
        # TODO: figure out this part
        score_meta_doc = {'$meta': 'textScore'}
        movies = db.movies.find(
            filter=filters, projection={'score': score_meta_doc}
        ).sort([('score', score_meta_doc)])
    else:
        movies = db.movies.find(filter=filters).sort()

    total_num_of_movies = movies.count()

    # Only return the movie list on the given page
    page_movies = movies.skip(page * movies_per_page).limit(movies_per_page)
    return page_movies, total_num_of_movies


def get_movie(_id: int) -> dict:
    """
    Returns the movie with the given ID.
    :param _id: int
    :return:
    """
    try:
        return db.movies.find_one({'_id': _id})
    except InvalidId:
        return None


def get_all_genres():
    pipeline = [
        {
            '$unwind': '$genres'
        },
        {
            '$project': {
                '_id': 0,
                'genres': 1
            }},
        {
            '$group': {
                '_id': None,
                'genres': {
                    '$addToSet': '$genres'
                }
            }
        }
    ]
    return list(db.movies.aggregate(pipeline))[0]['genres']


def get_user(email: str):
    """
    Returns the user with the given email.
    :param email: str
    :return:
    """
    return db.users.find_one({'email': email})
