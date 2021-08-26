import asyncio
from aiohttp.web import Request
import time
from unittest import TestCase
from wax.component.security import security_middleware, AuthUser
from wax.jwt_util import JWTUtil


async def handler_stub(request):
    return {'auth': request['auth']}


class RequestStub(dict):
    def __init__(self, method, path, auth_token=None):
        super().__init__()
        self.method = method
        self.path = path
        if auth_token:
            self.headers = {'Authorization': f'Bearer {auth_token}'}


class TestSecurityMiddleware(TestCase):
    def test_success(self):
        token = JWTUtil(None).encrypt(7, 'USER', int(time.time())+99)
        request_stub = RequestStub('GET', '/app/me', token)
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(security_middleware(request_stub, handler_stub))
        self.assertEqual(result, {'auth': AuthUser(user_id=7, role='USER')})
        loop.close()
