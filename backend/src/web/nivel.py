# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def index(_write_tmpl):
    _write_tmpl('templates/nivel.html')


def facil(_write_tmpl):
    _write_tmpl('templates/nivel.html', {'level': 'easy'})


def medio(_write_tmpl):
    _write_tmpl('templates/nivel.html', {'level': 'medium'})


def dificil(_write_tmpl):
    _write_tmpl('templates/nivel.html', {'level': 'hard'})


def adicao(_req, _write_tmpl, level):
    _write_tmpl('templates/adicao.html', {'level': level, 'kind': 'addition'})


def subtracao(_write_tmpl, level):
    _write_tmpl('templates/subtracao.html', {'level': level, 'kind': 'subtraction'})


def multiplicacao(_write_tmpl, level):
    _write_tmpl('templates/multiplicacao.html', {'level': level, 'kind': 'multiplication'})


def divisao(_write_tmpl, level):
    _write_tmpl('templates/divisao.html', {'level': level, 'kind': 'division'})
