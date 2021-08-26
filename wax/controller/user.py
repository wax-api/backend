from aiohttp.web import Request, Response, json_response, HTTPBadRequest
from wax.component.jwt import JWTUtil
from wax.component.pg import pg_cursor
from wax.component.security import auth_user
from wax.utils import timestamp
from wax.json_util import json_dumps
from wax.mapper.user import UserMapper


def wax_endpoint(endpoint):
    def f(g):
        return g
    return f


@wax_endpoint({
    'method': 'POST',
    'path': '/login',
    'requestBody': {
        'schema': {
            'email!': 'string',
            'password!': 'string'
        }
    },
    'response': {
        '200': {
            'schema': {
                'token': 'string'
            }
        }
    }
})
async def login(request: Request) -> Response:
    req_data = await request.json()
    user_mapper = UserMapper(request)
    user_db = await user_mapper.select_by_id(id=1)
    token = JWTUtil.from_(request.app).encrypt(user_db['id'], 'USER', timestamp(86400))
    return json_response({'token': token})


@wax_endpoint({
    'method': 'GET',
    'path': '/app/me',
    'response': {
        '200': {
            'schema': {
                'id': 'integer',
                'avatar': 'string',
                'truename': 'string',
                'email': 'string',
                'acl': 'string',
                'createdAt': 'string',
                'updatedAt': 'string',
            }
        }
    }
})
async def me_info(request: Request) -> Response:
    user_mapper = UserMapper(request)
    user_db = await user_mapper.select_by_id(id=auth_user(request).user_id)
    if not user_db:
        return HTTPBadRequest(text='当前用户不存在')
    return json_response(user_db, dumps=json_dumps)
