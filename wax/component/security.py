from aiohttp.web import middleware, Request, HTTPForbidden, HTTPNotFound, HTTPUnauthorized
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


@middleware
async def security_middleware(request: Request, handler):
    from wax.mapper.acl import ACLMapper
    from wax.mapper.apiacl import APIACLMapper
    try:
        token = left_strip(request.headers['Authorization'], 'Bearer ')
        payload = get_request_ctx(request, JWTUtil, 'jwtutil').decrypt(token)
        user_id = payload['uid']
        auth_user = AuthUser(user_id=user_id, role=payload['sub'], acl=[])
        set_request_ctx(request, type_=AuthUser, name='auth_user', instance=auth_user)
    except:
        auth_user = AuthUser(user_id=0, role='GUEST', acl=['G'])
        set_request_ctx(request, type_=AuthUser, name='auth_user', instance=auth_user)
    if auth_user.user_id:
        aclmapper = get_request_ctx(request, ACLMapper, 'aclmapper')
        acl_db = await aclmapper.select_by_user_id(user_id=auth_user.user_id)
        if not acl_db:
            raise HTTPUnauthorized()
        auth_user.acl.extend(acl_db['acl'])
    apiaclmapper = get_request_ctx(request, APIACLMapper, 'apiaclmapper')
    apiacl_db = await apiaclmapper.select_unique(method=request.method, path=request.path)
    if not request.path.startswith('/public/'):
        if not apiacl_db:
            raise HTTPNotFound()
        for api_acl in apiacl_db['acl']:
            re_pattern = '^' + api_acl.replace('*', '.*') + '$'
            if any(re.match(re_pattern, user_acl) for user_acl in auth_user.acl):
                break
        else:
            if auth_user.user_id:
                raise HTTPForbidden()
            else:
                raise HTTPUnauthorized()
    return await handler(request)
