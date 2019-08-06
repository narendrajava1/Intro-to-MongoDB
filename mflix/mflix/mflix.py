# -*- coding: utf-8 -*-

"""
Flask Application module.
"""

from flask import Flask, redirect, render_template, request, url_for
import flask_login

import mflix.db as db

MOVIES_PER_PAGE = 20

app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.route('/')
def show_movies():
    try:
        page = int(request.args.get('page'))
    except (TypeError, ValueError) as e:
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


@app.route('/movies/<id>', method=['GET', 'POST'])
@flask_login.login_required
def show_movie(id):
    movie = db.get_movie(id)
    pass


@app.route('/movies/<id>/comments/<comment_id>/delete', methods=['POST'])
@flask_login.login_required
def delete_movie_comment(id, comment_id):
    db.delete_comment_from_movie(id, comment_id)
    return redirect(url_for('show_movie', id=id))
