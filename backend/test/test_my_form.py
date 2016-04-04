# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import unittest
from web.models import MathProblem


class MathProblemTests(unittest.TestCase):

    def test_math_problem_sum_easy(self):
        math_problem = MathProblem('easy', 'sum')

        self.assertIn(math_problem.number_one, xrange(0, 10))


if __name__ == '__main__':
    unittest.main()
