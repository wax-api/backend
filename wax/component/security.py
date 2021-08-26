from aiohttp.web import middleware, Request, HTTPForbidden
import re
from wax.jwt_util import JWTUtil
from wax.utils import left_strip
from dataclasses import dataclass


@dataclass
class AuthUser:
    user_id: int
    role: str


AUTH_RULES = [  # # rules.item => (method, pattern, roles)
    ('*', '/login', None),
    ('*', '/app/**', ['USER']),
    ('*', '/public/**', None),
]


@middleware
async def security_middleware(request: Request, handler):
    try:
        token = left_strip(request.headers['Authorization'], 'Bearer ')
        payload = JWTUtil(None).decrypt(token)
        request['auth'] = AuthUser(user_id=payload['uid'], role=payload['sub'])
    except:
        request['auth'] = None
    for method, pattern, roles in AUTH_RULES:
        re_pattern = '^' + pattern.replace('/**', '(/.*)?') + '$'
        if (method == '*' or method == request.method) and re.match(re_pattern, request.path):
            if roles is None or (request['auth'] and request['auth'].role in roles):
                return await handler(request)
            else:
                return HTTPForbidden()
