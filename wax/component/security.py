from aiohttp.web import middleware, Request, HTTPForbidden, HTTPBadRequest
import re
from wax.component.jwt import JWTUtil
from wax.mapper.user import UserMapper
from wax.utils import left_strip
from dataclasses import dataclass


@dataclass
class AuthUser:
    user_id: int
    role: str
    acl: list


class Security:
    refname = 'wax.Security'
    auth_refname = f'{refname}.auth'


AUTH_RULES = [  # # rules.item => (method, pattern, roles)
    ('*', '/login', None),
    ('*', '/app/**', ['USER']),
    ('*', '/public/**', None),
]


@middleware
async def security_middleware(request: Request, handler):
    try:
        token = left_strip(request.headers['Authorization'], 'Bearer ')
        payload = JWTUtil.from_(request.app).decrypt(token)
        user_mapper = UserMapper(request)
        user_db = await user_mapper.select_by_id(id=payload['uid'])
        if not user_db:
            raise HTTPBadRequest(text='current user is deleted')
        request[Security.auth_refname] = AuthUser(user_id=payload['uid'], role=payload['sub'], acl=user_db['acl'])
    except:
        pass
    for method, pattern, roles in AUTH_RULES:
        re_pattern = '^' + pattern.replace('/**', '(/.*)?') + '$'
        if (method == '*' or method == request.method) and re.match(re_pattern, request.path):
            if roles is None or (authorized(request) and auth_user(request).role in roles):
                return await handler(request)
            else:
                return HTTPForbidden()


def authorized(request) -> bool:
    return Security.auth_refname in request


def auth_user(request) -> AuthUser:
    return request[Security.auth_refname]
