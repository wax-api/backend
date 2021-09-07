from aiohttp.web import middleware, Request, HTTPForbidden, HTTPBadRequest
import re
from wax.component.jwt import JWTUtil
from wax.utils import left_strip
from wax.inject_util import get_request_ctx, set_request_ctx
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
    from wax.mapper.acl import ACLMapper
    try:
        token = left_strip(request.headers['Authorization'], 'Bearer ')
        payload = get_request_ctx(request, JWTUtil, 'jwtutil').decrypt(token)
        user_id = payload['uid']
        auth_user = AuthUser(user_id=user_id, role=payload['sub'], acl=['U', f'U{user_id}'])
        set_request_ctx(request, type_=AuthUser, name='auth_user', instance=auth_user)
    except:
        auth_user = AuthUser(user_id=0, role='GUEST', acl=['G'])
        set_request_ctx(request, type_=AuthUser, name='auth_user', instance=auth_user)
    if auth_user.user_id:
        aclmapper = get_request_ctx(request, ACLMapper, 'aclmapper')
        user_db = await aclmapper.select_by_user_id(user_id=auth_user.user_id)
        if not user_db:
            raise HTTPBadRequest(text='current user is deleted')
        auth_user.acl.clear()
        auth_user.acl.extend(user_db['acl'])
    for method, pattern, roles in AUTH_RULES:
        re_pattern = '^' + pattern.replace('/**', '(/.*)?') + '$'
        if (method == '*' or method == request.method) and re.match(re_pattern, request.path):
            if roles is None or (auth_user.user_id and auth_user.role in roles):
                return await handler(request)
            else:
                return HTTPForbidden()
