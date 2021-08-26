"""
Copyright (c) 2021  Chongqing Parsec Inc.
wax-backend is licensed under the Lesspl Public License(v0.3).
You may obtain a copy of Lesspl Public License(v0.3) at: http://www.lesspl.org
"""


from unittest import TestCase
from wax.utils import eafp, left_strip, setdefault, randstr


class TestEafp(TestCase):
    def test_success(self):
        result = eafp(lambda: [][1], default='error')
        self.assertEqual(result, 'error')
        result = eafp(lambda: [1, 2][1], default=0)
        self.assertEqual(result, 2)


class TestLeftStrip(TestCase):
    def test_success(self):
        result = left_strip('abcde', 'abc')
        self.assertEqual(result, 'de')
        result = left_strip('abcde', 'cba')
        self.assertEqual(result, 'abcde')


class TestRandstr(TestCase):
    def test_success(self):
        result = randstr('a9Y', 9)
        self.assertIsInstance(result, str)
        self.assertEqual(9, len(result))
        self.assertEqual('', result.strip('a9Y'))


class TestSetDefault(TestCase):
    def test_success(self):
        map = {}
        result = setdefault(map, 'aa', lambda: 7)
        self.assertEqual(result, 7)
        self.assertDictEqual(map, {'aa': 7})
        items = [9]
        result = setdefault(map, 'aa', lambda: items.clear() or 3)
        self.assertEqual(result, 7)
        self.assertDictEqual(map, {'aa': 7})
        self.assertListEqual(items, [9])
