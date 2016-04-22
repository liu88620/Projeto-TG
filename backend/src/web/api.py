# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json

from google.appengine.ext import ndb
from web.models import MathProblem, MathProblemSet


def get_problem_set(_resp, level=None, kind=None, quantity=10):
    problems = []
    for _ in range(int(quantity)):
        math_problem = MathProblem(level=level, kind=kind)
        math_problem.generate_problem()
        problems.append(math_problem)

    keys = ndb.put_multi(problems)

    math_problem_set = MathProblemSet(problems=keys)
    math_problem_set.put()
    first_problem = math_problem_set.get_next_problem(0)

    response = {
        'problem': first_problem.to_dict(),
        'math_problem_set_id': math_problem_set.key.id()
    }
    _resp.write(json.dumps(response))


def get_problem(_resp, problem_set_id, index):
    math_problem_set = MathProblemSet.get_by_id(long(problem_set_id))

    problem = math_problem_set.get_next_problem(int(index))
    if problem is not None:
        return _resp.write(json.dumps(problem.to_dict()))


def save_time_spent(_handler, time_spent, problem_set_id):
    math_problem_set = MathProblemSet.get_by_id(long(problem_set_id))
    math_problem_set.time_spent = float(time_spent)    
    math_problem_set.put()


def solve_problem(_resp, problem_set_id, problem_id=None, answer=None):
    math_problem_set = MathProblemSet.get_by_id(long(problem_set_id))
    math_problem = MathProblem.get_by_id(long(problem_id))
    is_correct = math_problem.answer_problem(int(answer))
    if is_correct:
        math_problem_set.right_answers += 1
        math_problem_set.put()
    response = {'is_correct': is_correct}
    _resp.write(json.dumps(response))