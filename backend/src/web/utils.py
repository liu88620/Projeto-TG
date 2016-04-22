# coding: utf-8

from google.appengine.api import users


def login_user(_handler):
    user = users.get_current_user()
    if not user:
        return _handler.redirect(users.create_login_url('/'))