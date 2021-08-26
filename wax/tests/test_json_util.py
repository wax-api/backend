"""
Copyright (c) 2021  Chongqing Parsec Inc.
wax-backend is licensed under the Lesspl Public License(v0.3).
You may obtain a copy of Lesspl Public License(v0.3) at: http://www.lesspl.org
"""


from unittest import TestCase
from wax.json_util import json_dumps, _default_serial
from datetime import date, time


class TestJSONUtil(TestCase):
    def test_success(self):
        someday = date(2021, 2, 28)
        self.assertEqual(_default_serial(someday), '2021-02-28')
        sometime = time(23, 59, 0)
        self.assertEqual(_default_serial(sometime), '23:59:00')
        dumped = json_dumps({'now': someday})
        self.assertEqual(dumped, '{"now": "2021-02-28"}')
