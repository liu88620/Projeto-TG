# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from web.models import MathProblemSet


def index(_write_tmpl, math_problem_set_id):
    math_problem_set  = MathProblemSet.get_by_id(long(math_problem_set_id))
    _write_tmpl('templates/resultados.html', {'time_spent': math_problem_set.time_spent,
                                              'right_answers': math_problem_set.right_answers})

