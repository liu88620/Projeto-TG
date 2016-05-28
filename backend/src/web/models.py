# coding: utf-8

import operator
from random import randint, randrange, shuffle, choice
from google.appengine.ext import ndb
from web.utils import divider_int


kind_to_operation = {
    'addition': operator.add,
    'subtraction': operator.sub,
    'multiplication': operator.mul,
    'division': operator.div
}


class MathProblemSet(ndb.Model):
    problems = ndb.KeyProperty(repeated=True)
    time_spent = ndb.FloatProperty(required=False)
    right_answers = ndb.IntegerProperty(required=False, default=0)

    def get_next_problem(self, index):
        try:
            problem = self.problems[index]
        except IndexError:
            return None
        else:
            return problem.get()

    def to_dict(self, *args, **kwargs):
        dic = super(MathProblemSet, self).to_dict()
        dic['id'] = self.key.id()
        return dic

    def get_first_problem(self):
        return self.problems[0].get()

    def get_problem_kind(self):
        # assume que todos os problemas
        # possuem mesmo kind

        return self.get_first_problem().kind

    def get_problem_level(self):
        return self.get_first_problem().level

class MathProblem(ndb.Model):

    level = ndb.StringProperty(required=True)
    kind = ndb.StringProperty(required=True)
    number_one = ndb.IntegerProperty()
    number_two = ndb.IntegerProperty()
    answer = ndb.IntegerProperty()
    choices = ndb.IntegerProperty(repeated=True)

    def __init__(self, *args, **kwargs):
        super(MathProblem, self).__init__(*args, **kwargs)

    def to_dict(self, *args, **kwargs):
        dic = super(MathProblem, self).to_dict()
        dic['id'] = self.key.id()
        return dic

    def generate_problem(self):
        operation = kind_to_operation[self.kind]
        range1, range2 = randrange(10), randrange(2, 10)
        start, end = 0, 10

        if self.kind in ('addition', 'subtraction'):
            if self.level == 'medium':
                range1, range2 = randrange(19), randrange(19)
                start, end = 10, 19
            if self.level == 'hard':
                range1, range2 = randrange(199), randrange(199)
                start, end = 100, 199
        if self.kind == 'division':
            if self.level in ('easy', 'medium'):
                range1 = randrange(2, 100, 2)
                range2 = choice(divider_int(range1))
                start, end = 0, 10
            elif self.level == 'hard':
                range1 = randrange(100, 1000, 2)
                range2 = choice(divider_int(range1))
                start, end = 10, 1000
        if self.kind == 'multiplication':
             if self.level == 'easy':
                 range1, range2 = randint(0, 10), randint(0, 10)
                 start, end = 0, 50
             if self.level == 'medium':
                 range1, range2 = randint(0, 100), randint(0, 10)
                 start, end = 50, 150
             if self.level == 'hard':
                 range1, range2 = randint(0, 100), randint(0, 50)
                 start, end = 100, 900
        self.generate_answer(range1, range2, operation)
        self.generate_choices(start, end)
        shuffle(self.choices)

    def generate_choices(self, start, end, step=1, quant_choices=2):
        while len(self.choices) <= quant_choices:
            number = randrange(start, end, step)
            if number not in self.choices:
                self.choices.append(number)

    def generate_answer(self, range1, range2, operation):
        self.number_one = range1
        self.number_two = range2
        self.answer = operation(self.number_one, self.number_two)
        self.choices.append(self.answer)

    def answer_problem(self, answer):
        try:
            answer = float(answer)
        except ValueError:
            answer = int(answer)
        return answer == self.answer