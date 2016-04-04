# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from web.models import MathProblem


def create_problem(_resp, level=None, kind=None):
    math_problem = MathProblem(level=level, kind=kind)
    key = math_problem.put()

    _resp.write(json.dumps(
        {
            'id': key.id(),
            'number_one': math_problem.number_one,
            'number_two': math_problem.number_two,
            'choices': math_problem.choices,
            'kind': math_problem.kind
        })
    )


def solve_problem(_resp, id=None, answer=None):
    math_problem = MathProblem.get_by_id(long(id))
    response = {'is_correct': math_problem.answer_problem(answer)}
    math_problem.key.delete()
    _resp.write(json.dumps(response))