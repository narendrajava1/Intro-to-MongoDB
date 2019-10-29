# -*- coding: utf-8 -*-

"""
Interface module with MongoDB.
"""

import os
from datetime import datetime
from typing import List, Optional, Tuple

from bson.errors import InvalidId
from bson.objectid import ObjectId
from pymongo import DESCENDING, MongoClient
from pymongo.errors import DuplicateKeyError

MOVIE_COMMENT_CACHE_LIMIT = 10

try:
    db = MongoClient(os.environ['MFLIX_DB_URI'])[os.environ['DB_NAME']]
except KeyError:
    raise Exception("You haven't configured your MFLIX_DB_URI!")


def get_page_movies(filters: dict, movies_per_page: int,
                    page: int) -> Tuple[list, int]:
    """
    Returns a movie list on the given page based on the given filters and number
    of movies per page.
    :param filters: dict
    :param movies_per_page: int
    :param page: int
    :return: tuple
    """
    if '$text' in filters:
        # TODO: Figure this out
        score_meta_doc = {'$meta': 'textScore'}
        movies = db.movies.find(filters, projection={'score': score_meta_doc})\
            .sort([('score', score_meta_doc)])
    else:
        movies = db.movies.find(filters)\
            .sort('tomatoes.viewers.numReviews', direction=DESCENDING)

    total_num_of_movies = movies.count()

    # Only return the movie list on the given page
    page_movies = movies.skip(page * movies_per_page).limit(movies_per_page)
    return page_movies, total_num_of_movies


def get_movie(_id: str) -> Optional[dict]:
    """
    Returns the movie with the given ID.
    :param _id: str
    :return: dict or None
    """
    try:
        return db.movies.find_one({'_id': ObjectId(_id)})
    except InvalidId:
        return None


def get_all_genres() -> List[str]:
    """
    Returns all the genres.
    :return: list[str]
    """
    pipeline = [
        {
            '$unwind': '$genres'
        },
        {
            '$project': {
                '_id': 0,
                'genres': 1
            }
        },
        # TODO: Figure out this "group"
        {
            '$group': {
                '_id': None,
                'genres': {
                    '$addToSet': '$genres'
                }
            }
        }
    ]
    # After the pipeline, there is only one document, containing only one field
    # "genres", which is array containing all the different genres.
    return list(db.movies.aggregate(pipeline))[0]['genres']


def get_user(email: str) -> Optional[dict]:
    """
    Returns the user with the given email.
    :param email: str
    :return: dict or None
    """
    return db.users.find_one({'email': email})  # Could be None


def add_user(name: str, email: str, hashedpw: str) -> dict:
    """
    Adds a user with the given name, email and hashed password.
    :param name: str
    :param email: str
    :param hashedpw: str
    :return: dict
    """
    new_user = {
        'name': name,
        'email': email,
        'pw': hashedpw
    }
    try:
        db.users.insert_one(new_user)
        return {'success': True}
    except DuplicateKeyError:
        return {'error': 'A user with the given email already exists'}


def get_movie_comments(_id: str) -> Optional[List[dict]]:
    """
    Returns the comments of the given movie, from most-recent to least-recent.
    :param _id: int
    :return: list[dict] or None
    """
    try:
        return db.comments.find({'movie_id': ObjectId(_id)})\
            .sort('date', direction=DESCENDING)
    except InvalidId:
        return None


def add_comment_to_movie(movie_id: str, user, comment: str,
                         date: datetime) -> None:
    """
    Adds a comment to the given movie from the given user, on the given date.
    :param movie_id: str
    :param user: User
    :param comment: str
    :param date: datetime
    :return: None
    """
    movie = get_movie(movie_id)
    if movie:
        movie_id = ObjectId(movie_id)
        # 1. Add a new comment to "comments" collection
        new_comment = {
            '_id': f'{movie_id}-{user.name}-{date.timestamp()}',
            'movie_id': movie_id,
            'name': user.name,
            'email': user.email,
            'text': comment,
            'date': date
        }
        db.comments.insert_one(new_comment)
        # 2. At the same time, update the corresponding movie in "movies"
        # collection
        movie_update = {
            # 2.1 Increment the comment count on the movie
            '$inc': {
                'num_mflix_comments': 1
            },
            # 2.2 Update the cached comments on the movie
            '$push': {
                'comments': {
                    '$each': [new_comment],
                    '$sort': {'date': -1},
                    '$slice': MOVIE_COMMENT_CACHE_LIMIT
                }
            }
        }
        db.movies.update_one({'_id': movie_id}, update=movie_update)


def delete_comment_from_movie(movie_id: str, comment_id: str) -> None:
    """
    Deletes the given comment from the given movie.
    :param movie_id: str
    :param comment_id: str
    :return: None
    """
    # 1. Delete the comment from "comments" collection
    comment_id = ObjectId(comment_id)
    db.comments.delete_one({'_id': comment_id})

    # 2. At the same time, update the corresponding movie in "movies" collection

    # 2.1 Decrement the comment count on the movie
    movie_id = ObjectId(movie_id)
    movie_update = {
        '$inc': {
            'num_mflix_comments': -1
        }
    }
    db.movies.update_one({'_id': movie_id}, update=movie_update)

    # Check whether the comment is cached on the movie
    movie = db.movies.find_one({'comments._id': comment_id})
    if movie:
        # 2.2 If so, update the cached comments on the movie
        updated_comments = db.comments.find({'movie_id': movie_id})\
            .sort('date', direction=DESCENDING).limit(MOVIE_COMMENT_CACHE_LIMIT)
        movie_update = {
            '$set': {
                'comments': list(updated_comments)
            }
        }
        db.movies.update_one({'_id': movie_id}, update=movie_update)
