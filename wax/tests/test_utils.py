"""
Copyright (c) 2021  Chongqing Parsec Inc.
wax-backend is licensed under the Lesspl Public License(v0.2).
You may obtain a copy of Lesspl Public License(v0.2) at: http://www.lesspl.org
"""


from unittest import TestCase
from wax.utils import eafp


class TestEafp(TestCase):
    def test_success(self):
        result = eafp(lambda: [][1], default='error')
        self.assertEqual(result, 'error')
        result = eafp(lambda: [1, 2][1], default=0)
        self.assertEqual(result, 2)
