# -*- coding: utf-8 -*-

"""
Flask application module.
"""

from typing import Union

import flask_bcrypt
import flask_login
from flask import redirect, render_template, request, url_for

import mflix.db as db
from .mflix import app

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

bcript = flask_bcrypt.Bcrypt(app)


class User(flask_login.UserMixin):
    # TODO: Figure this out
    pass


def create_user_object(user_doc: dict) -> User:
    """
    Creates a User object from the given user document.
    :param user_doc: dict
    :return: User
    """
    user_obj = User()
    user_obj.id = user_doc['email']
    user_obj.name = user_doc['name']
    user_obj.first_name = user_doc['name'].split(', ')[0]
    user_obj.email = user_doc['email']
    return user_obj


# TODO: Figure this out
@login_manager.user_loader
def user_loader(email: str) -> Union[User, None]:
    user_doc = db.get_user(email)
    if not user_doc:
        return
    return create_user_object(user_doc)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Sign-up page.
    :return:
    """
    if request.method == 'GET':
        return redirect(url_for('login'))

    # When sending "POST" request, request.form
    name = request.form['name']
    email = request.form['email']
    pw = request.form['password']

    if len(pw) < 8:
        return render_template(
            'login.html', signuperror='Password must be at least 8 characters.'
        )
    elif pw != request.form['confirmed_password']:
        return render_template(
            'login.html', signuperror='Make sure to confirm the password!'
        )

    insertion_result = db.add_user(
        name, email, hashedpw=bcript.generate_password_hash(pw)
    )
    if 'error' in insertion_result:
        return render_template(
            'login.html', signuperror=insertion_result['error']
        )

    new_user = db.get_user(email)
    new_user_obj = create_user_object(new_user)
    flask_login.login_user(new_user)
    return redirect(url_for('show_movies'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in Page.
    :return:
    """
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    pw = request.form['password']

    user_doc = db.get_user(email)
    if not user_doc:
        return render_template(
            'login.html', loginerror='Make sure your email is correct.'
        )
    if bcript.check_password_hash(user_doc['pw'], pw):
        return render_template(
            'login.html', loginerror='Make sure your password is correct.'
        )

    user_obj = create_user_object(user_doc)
    flask_login.login_user(user_obj)
    return redirect(url_for('show_movies'))


@app.route('/logout', methods=['GET'])
@flask_login.login_required
def logout():
    """
    Logout page.
    (Log-in required)
    When a "GET" request is forwarded to "/logout", this function gets called.
    :return:
    """
    flask_login.logout_user()
    return redirect(url_for('show_movies'))


@app.route('/profile', methods=['GET'])
@flask_login.login_required
def profile():
    """
    Profile page.
    (Log-in required)
    When a "GET" request is forwarded to "/profile", this function gets called.
    :return:
    """
    return render_template('profile.html')


# TODO: Figure this out
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('splash_screen.html')
