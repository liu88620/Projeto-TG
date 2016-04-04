# coding: utf-8

from random import randint, randrange
from google.appengine.ext import ndb


class MathProblem(ndb.Model):

    level = ndb.StringProperty(required=True)
    kind = ndb.StringProperty(required=True)
    number_one = ndb.IntegerProperty()
    number_two = ndb.IntegerProperty()
    answer = ndb.IntegerProperty()
    choices = ndb.IntegerProperty(repeated=True)

    def __init__(self, *args, **kwargs):
        super(MathProblem, self).__init__(*args, **kwargs)
        self._generate_problem()

    def _set_numbers_values(self, value_one, value_two):
        self.number_one = value_one
        self.number_two = value_two

    def _generate_problem(self):
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
                self.choices = [randint(0, 10) for _ in xrange(2, 50, 2)]
            elif self.level == 'hard':
                self._set_numbers_values(randrange(100, 1000, 2), randrange(2, 100, 2))
                self.choices = [randint(0, 10) for _ in xrange(2, 100, 2)]
            self.answer = self.number_one // self.number_two
        self.choices.append(self.answer)

    def answer_problem(self, answer):
        try:
            answer = float(answer)
        except ValueError:
            answer = int(answer)
        return answer == self.answer