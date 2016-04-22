# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from web.decorators import logged


def cadastra(_write_tmpl):
    _write_tmpl('templates/cadastro.html')


@logged
def index(_handler, _write_tmpl):
    _write_tmpl('templates/index.html')


def params(_resp, *args, **kwargs):
    _resp.write(args)
    _resp.write(kwargs)