# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from web.utils import login_user


def index(_handler, _write_tmpl):
    login_user(_handler)
    _write_tmpl('templates/index.html')


def params(_resp, *args, **kwargs):
    _resp.write(args)
    _resp.write(kwargs)