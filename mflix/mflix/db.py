# -*- coding: utf-8 -*-

"""
Interface module with MongoDB.
"""

import os
from datetime import datetime
from typing import Tuple

from bson.errors import InvalidId
from bson.objectid import ObjectId
from pymongo import DESCENDING, MongoClient

MOVIE_COMMENT_CACHE_LIMIT = 10

try:
    db = MongoClient(os.environ['MFLIX_DB_URI']).mflix
except KeyError:
    raise Exception("You haven't configured your MFLIX_DB_URI!")


def get_page_movies(filters: dict, page: int,
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


def get_movie(_id: str):
    """
    Returns the movie with the given ID.
    :param _id: str
    :return:
    """
    try:
        return db.movies.find_one({'_id': ObjectId(_id)})
    except InvalidId:
        return None


def get_movie_comments(_id: str):
    """
    Returns the comments of the given movie, from most-recent to least-recent.
    :param _id: int
    :return:
    """
    try:
        return db.comments.find({'movie_id': ObjectId(_id)})\
            .sort('date', direction=DESCENDING)
    except InvalidId:
        return None


def get_user(email: str):
    """
    Returns the user with the given email.
    :param email: str
    :return:
    """
    return db.users.find_one({'email': email})  # Could be None


def add_comment_to_movie(movie_id: str, user, comment: str,
                         date: datetime) -> None:
    """
    Adds a comment to the given movie from the given user, on the given date.
    :param movie_id: str
    :param user:
    :param comment: str
    :param date: datetime
    :return: None
    """
    movie = get_movie(movie_id)
    if movie:
        movie_id = ObjectId(movie_id)
        comment_doc = {
            '_id': f'{movie_id}-{user.name}-{datetime.timestamp()}',
            'movie_id': movie_id,
            'name': user.name,
            'email': user.email,
            'text': comment,
            'date': date
        }
        db.comments.insert_one(comment_doc)

        movie_update = {
            # Increment "num_flix_comments" count on the movie
            '$inc': {
                'num_mflix_comments': 1
            },
            '$push': {
                'comments': {
                    '$each': [comment_doc],
                    '$sort': {'date': -1},
                    '$slice': MOVIE_COMMENT_CACHE_LIMIT
                }
            }
        }
        db.movies.update_one(filter={'_id': movie_id}, update=movie_update)


def delete_comment_from_movie(movie_id: str, comment_id: str) -> None:
    """
    Deletes the given comment from the given movie.
    :param movie_id: str
    :param comment_id: str
    :return: None
    """
    # Delete the comment from "comments" collection
    comment_id = ObjectId(comment_id)
    db.comments.delete_one({'_id': comment_id})

    # Decrement "num_mflix_comment" count on the movie
    movie_id = ObjectId(movie_id)
    movie_update = {
        '$inc': {
            'num_mflix_comments': -1
        }
    }
    db.movies.update_one(filter={'_id': movie_id}, update=movie_update)

    # Check whether the comment is on the movie in "movies" collections
    movie = db.movies.find_one({'comments._id': comment_id})
    if movie:
        updated_comments = db.comments.find({'movie_id': movie_id})\
            .sort('date', direction=DESCENDING).limit(MOVIE_COMMENT_CACHE_LIMIT)
        movie_update = {
            '$set': {
                'comments': list(updated_comments)
            }
        }
        db.movies.update_one(filter={'_id': movie_id}, update=movie_update)
