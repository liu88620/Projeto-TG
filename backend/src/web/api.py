# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api.datastore_errors import BadValueError
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


def solve_problem(_resp, problem_id=None, answer=None):
    try:
        # por algum motivo maluco ele falha da primeira vez
        math_problem = MathProblem.get_by_id(long(problem_id))
    except BadValueError:
        math_problem = MathProblem.get_by_id(long(problem_id))
    response = {'is_correct': math_problem.answer_problem(int(answer))}
    math_problem.key.delete()
    _resp.write(json.dumps(response))