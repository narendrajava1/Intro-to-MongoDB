# -*- coding: utf-8 -*-

"""
Flask models module.
"""

from typing import Optional

from flask_login import UserMixin

import mflix.db as db
from . import login_manager


class User(UserMixin):
    """
    Self-defined User class, which represents a user of the application.
    """
    pass


@login_manager.user_loader
def user_loader(email: str) -> Optional[User]:
    """
    Flask-Login user loader for reloading the logged-in user from the session.
    :param email: str
    :return: User or None
    """
    user_doc = db.get_user(email)
    if not user_doc:
        return None
    return create_user_object(user_doc)


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
