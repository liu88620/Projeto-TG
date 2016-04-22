# coding: utf-8

from random import randint, randrange, shuffle
from google.appengine.ext import ndb
from google.appengine.api.datastore_errors import BadValueError



def generate_choices(start, end, step=1):
    range_gen = randrange(start, end, step)
    choices = []
    while len(choices) != 2:
        number = next(range_gen)
        if number not in choices:
            choices.append(number)
    return choices


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

    def _set_numbers_values(self, value_one, value_two):
        self.number_one = value_one
        self.number_two = value_two

    def generate_problem(self):
        if self.kind in ('addition', 'subtraction'):
            if self.level == 'easy':
                self._set_numbers_values(randint(0, 10), randint(0, 10))
                self.choices = [randint(0, 10) for _ in xrange(2)]
            elif self.level == 'medium':
                self._set_numbers_values(randint(0, 19), randint(0, 19))
                self.choices = [randint(0, 19) for _ in xrange(2)]
            elif self.level == 'hard':
                self._set_numbers_values(randint(0, 199), randint(0, 199))
                self.choices = [randint(0, 199) for _ in xrange(2)]
            if self.kind == 'addition':
                self.answer = self.number_one + self.number_two
            else:
                self.answer = self.number_one - self.number_two
        if self.kind == 'multiplication':
            if self.level == 'easy':
                self._set_numbers_values(randint(0, 10), randint(0, 10))
                self.choices = [randint(0, 50) for _ in xrange(2)]
            if self.level == 'medium':
                self._set_numbers_values(randint(0, 100), randint(0, 10))
                self.choices = [randint(50, 150) for _ in xrange(2)]
            if self.level == 'hard':
                self._set_numbers_values(randint(0, 100), randint(0, 50))
                self.choices = [randint(100, 900) for _ in xrange(2)]
            self.answer = self.number_one * self.number_two
        if self.kind == 'division':
            if self.level in ('easy', 'medium'):
                self._set_numbers_values(randrange(2, 100, 2), randrange(2, 4, 5, 10))
                self.choices = [randint(0, n) for n in xrange(2, 50, 2)]
            elif self.level == 'hard':
                self._set_numbers_values(randrange(100, 1000, 2), randrange(2, 100, 2))
                self.choices = [randint(0, n) for n in xrange(2, 50, 2)]
            self.answer = self.number_one // self.number_two
        self.choices.append(self.answer)
        shuffle(self.choices)

    def answer_problem(self, answer):
        try:
            answer = float(answer)
        except ValueError:
            answer = int(answer)
        return answer == self.answer