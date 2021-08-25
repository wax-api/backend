"""
Copyright (c) 2021  Chongqing Parsec Inc.
wax-backend is licensed under the Lesspl Public License(v0.3).
You may obtain a copy of Lesspl Public License(v0.3) at: http://www.lesspl.org
"""


import time
from unittest import TestCase
from wax.jwt_util import JWTUtil
from wax.utils import now_timestamp


class TestJWTUtil(TestCase):
    def test_success(self):
        jwt_util = JWTUtil(None)
        exp = now_timestamp() + 100
        token = jwt_util.encrypt(23, 'ADMIN', exp)
        self.assertTrue(isinstance(token, str) and len(token) > 30)
        payload = jwt_util.decrypt(token)
        self.assertDictEqual(payload, {'uid': 23, 'sub': 'ADMIN', 'exp': exp})
