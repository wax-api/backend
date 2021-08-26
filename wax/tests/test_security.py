import asyncio
import time
from unittest import TestCase
from wax.component.security import security_middleware, AuthUser
from wax.component.jwt import JWTUtil


async def handler_stub(request):
    return {'auth': request['auth']}


class RequestStub(dict):
    def __init__(self, method, path):
        super().__init__()
        self.method = method
        self.path = path
        self.app = {'config': {}}
        self.headers = {}


class TestSecurityMiddleware(TestCase):
    def test_success(self):
        request_stub = RequestStub('GET', '/app/me')
        token = JWTUtil.from_(request_stub.app).encrypt(7, 'USER', int(time.time()) + 99)
        request_stub.headers.update({'Authorization': f'Bearer {token}'})
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(security_middleware(request_stub, handler_stub))
        self.assertEqual(result, {'auth': AuthUser(user_id=7, role='USER')})
        loop.close()
