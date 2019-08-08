# -*- coding: utf-8 -*-

"""
Flask application module.
"""

from flask import Flask, redirect, render_template, request, url_for
import flask_login

import mflix.db as db

MOVIES_PER_PAGE = 20

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(SECRET_KEY='mflix-app-mongodb'))
app.config.from_envvar('MFLIX_SETTINGS', silent=True)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

from .auth import login, logout


@app.route('/', methods=['GET'])
def show_movies():
    """
    Mflix application home page.
    When a "GET" request is forwarded to "/", this function gets called.
    :return:
    """
    # Note!
    # When a "GET" request is forwarded, the URL may be carrying some arguments,
    # which is stored in "request.args"
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

    page_movies, total_num_of_movies = db.get_page_movies(
        filters, page, MOVIES_PER_PAGE
    )
    # TODO: implementation

    # all_genres = db.get_all_genres()

    return render_template('movies.html')


@app.route('/movies/<id>', methods=['GET', 'POST'])
@flask_login.login_required
def show_movie(id):
    # TODO: Pay attention to, when sending "POST" request, request.form
    return render_template(
        'movie.html', movie=db.get_movie(id),
        new_comment=request.form.get('comment')  # There may not be "comment", , and thus may not be "new_comment".
    )


@app.route('/movies/<id>/comments', methods=['GET', 'POST'])
@flask_login.login_required
def show_movie_comments(id):
    pass


@app.route('/movies/<id>/comments/<comment_id>/delete', methods=['POST'])
@flask_login.login_required
def delete_movie_comment(id, comment_id):
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


@app.route('/movies/watch/<id>', methods=['GET'])
@flask_login.login_required
def watch_movie(id):
    """
    Movie watch page.
    (Log-in required)
    When a "GET" request is forwarded to "/movies/watch/<id>", this function
    gets called.
    :return:
    """
    return render_template('watch_movie.html', movie=db.get_movie(id))
