"""
Copyright (c) 2021  Chongqing Parsec Inc.
wax-backend is licensed under the Lesspl Public License(v0.3).
You may obtain a copy of Lesspl Public License(v0.3) at: http://www.lesspl.org
"""

from unittest import TestCase
from wax.component.jwt import JWTUtil
from wax.utils import timestamp
from wax.inject_util import get_request_ctx


class RequestStub(dict):
    def __init__(self, method, path):
        super().__init__()
        self.method = method
        self.path = path
        self.app = {'config': {}}
        self.headers = {}


class TestJWTUtil(TestCase):
    def test_success(self):
        request_stub = RequestStub('GET', '/app/me')
        jwt_util = get_request_ctx(request_stub, JWTUtil, 'jwtutil')
        exp = timestamp(100)
        token = jwt_util.encrypt(23, 'ADMIN', exp)
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 30)
        payload = jwt_util.decrypt(token)
        self.assertDictEqual(payload, {'uid': 23, 'sub': 'ADMIN', 'exp': exp})
