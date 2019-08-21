# -*- coding: utf-8 -*-

"""
Flask application module.
"""

from datetime import datetime
from urllib.parse import urlencode

from flask import Flask, redirect, render_template, request, url_for
import flask_login

import mflix.db as db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mflix-app-mongodb'
# Override the configuration values from the configuration file, which is
# pointed by "MFLIX_SETTINGS" environment variable
app.config.from_envvar('MFLIX_SETTINGS', silent=True)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Since in "auth.py", we are importing "app" from this module, we have to import
# that "auth.py" module after we instantiated "app".
from .auth import login, logout


@app.route('/')
def show_movies():
    """
    Mflix application home page.
    When a "GET" request is forwarded to "/", this function gets called.
    :return:
    """
    movies_per_page = 20

    # Note!
    # When a "GET" request is forwarded, the URL may be carrying some arguments,
    # which is stored in "request.args".
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
    (Log-in required)
    :param id: str
    :return:
    """
    context = {
        'movie': db.get_movie(id)
    }
    if request.method == 'POST':
        # Note:
        # When a "POST" request is forwarded, the request is carrying the filled
        # form, stored in "request.form"
        context['new_comment'] = request.form['comment']
    return render_template('movie.html', **context)


@app.route('/movies/<id>/comments', methods=['GET', 'POST'])
@flask_login.login_required
def show_movie_comments(id: str):
    """
    Movie comments page.
    (Log-in required)
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


@app.route('/movies/<id>/comments/<comment_id>/delete', methods=['POST'])
@flask_login.login_required
def delete_movie_comment(id: str, comment_id: str):
    """
    Movie deletion page.
    (Log-in required)
    When a "POST" request is forwarded to
    "/movies/<id>/comments/<comment_id>/delete", this function gets called.
    :param id: str
    :param comment_id: str
    :return:
    """
    db.delete_comment_from_movie(id, comment_id)
    return redirect(url_for('show_movie', id=id))


@app.route('/movies/watch/<id>')
@flask_login.login_required
def watch_movie(id: str):
    """
    Movie watch page.
    (Log-in required)
    When a "GET" request is forwarded to "/movies/watch/<id>", this function
    gets called.
    :param id: str
    :return:
    """
    context = {
        'movie': db.get_movie(id)
    }
    return render_template('watch_movie.html', **context)
