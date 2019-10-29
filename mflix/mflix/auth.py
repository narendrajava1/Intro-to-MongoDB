# -*- coding: utf-8 -*-

"""
Authentication module.
"""

from typing import Optional

import flask_login
from flask import redirect, render_template, request, url_for

import mflix.db as db
from . import app, bcrypt, login_manager
from .models import create_user_object


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Sign-up page.
    :return:
    """
    if request.method == 'GET':
        return render_template('login.html')

    name = request.form['name']
    email = request.form['email']
    pw = request.form['password']

    if len(pw) < 8:
        return render_template(
            'login.html', signuperror='Password must be at least 8 characters.'
        )
    elif pw != request.form['confirm-password']:
        return render_template(
            'login.html', signuperror='Make sure to confirm the password!'
        )

    insertion_result = db.add_user(
        name, email, hashedpw=bcrypt.generate_password_hash(pw)
    )
    if 'error' in insertion_result:
        return render_template(
            'login.html', signuperror=insertion_result['error']
        )

    new_user_doc = db.get_user(email)
    new_user_obj = create_user_object(new_user_doc)
    flask_login.login_user(new_user_obj)
    return redirect(url_for('show_movies'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page.
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
    if bcrypt.check_password_hash(user_doc['pw'], pw):
        return render_template(
            'login.html', loginerror='Make sure your password is correct.'
        )

    user_obj = create_user_object(user_doc)
    flask_login.login_user(user_obj)
    return redirect(url_for('show_movies'))


@app.route('/profile')
@flask_login.login_required
def profile():
    """
    Profile page.
    :return:
    """
    return render_template('profile.html')


@app.route('/logout')
@flask_login.login_required
def logout():
    """
    Logout page.
    :return:
    """
    flask_login.logout_user()
    return redirect(url_for('show_movies'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    """
    Flask-Login unauthorized handler.
    When "login_required", this function handles unauthorized users, and
    redirect them to appropriate place.
    :return:
    """
    return render_template('splash_screen.html')
