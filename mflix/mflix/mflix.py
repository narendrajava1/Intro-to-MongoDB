# -*- coding: utf-8 -*-

"""
Flask application module.
"""

from datetime import datetime
from urllib.parse import urlencode

from flask import redirect, render_template, request, url_for
import flask_login

import mflix.db as db
from . import app


@app.route('/')
def show_movies():
    """
    Mflix application home page.
    :return:
    """
    movies_per_page = 20

    try:
        page = int(request.args.get('page'))
    except (TypeError, ValueError):
        page = 0

    filters = {}
    genre = request.args.get('genre')
    if genre:
        filters['genres'] = genre
    search = request.args.get('search')
    if search:
        filters['$text'] = {'$search': search}

    # For pagination
    args_copy = request.args.copy()
    args_copy['page'] = page - 1
    prev_page = urlencode(args_copy)
    args_copy['page'] = page + 1
    next_page = urlencode(args_copy)

    page_movies, total_num_of_movies = db.get_page_movies(
        filters, movies_per_page, page
    )

    all_genres = db.get_all_genres()

    context = {
        'total_num_of_entries': total_num_of_movies,
        'entries_per_page': movies_per_page,
        'page': page,
        'filters': filters,
        'movies': page_movies,
        'prev_page': prev_page,
        'next_page': next_page,
        'all_genres': all_genres
    }
    return render_template('movies.html', **context)


@app.route('/movies/<id>', methods=['GET', 'POST'])
@flask_login.login_required
def show_movie(id: str):
    """
    Movie detail page.
    :param id: str
    :return:
    """
    context = {
        'movie': db.get_movie(id)
    }
    if request.method == 'POST':
        context['new_comment'] = request.form['comment']
    return render_template('movie.html', **context)


@app.route('/movies/<id>/comments', methods=['GET', 'POST'])
@flask_login.login_required
def show_movie_comments(id: str):
    """
    Movie comments page.
    :param id: str
    :return:
    """
    if request.method == 'POST':
        comment = request.form['comment']
        db.add_comment_to_movie(
            id, flask_login.current_user, comment, datetime.now()
        )
        return redirect(url_for('show_movie', id=id))

    context = {
        'movie': db.get_movie(id),
        'comments': db.get_movie_comments(id)
    }
    return render_template('movie_comments.html', **context)


@app.route('/movies/<movie_id>/comments/<comment_id>/delete', methods=['POST'])
@flask_login.login_required
def delete_movie_comment(movie_id: str, comment_id: str):
    """
    Movie deletion page.
    :param movie_id: str
    :param comment_id: str
    :return:
    """
    db.delete_comment_from_movie(movie_id, comment_id)
    return redirect(url_for('show_movie', id=id))


@app.route('/movies/watch/<id>')
@flask_login.login_required
def watch_movie(id: str):
    """
    Movie watch page.
    :param id: str
    :return:
    """
    context = {
        'movie': db.get_movie(id)
    }
    return render_template('watch_movie.html', **context)
