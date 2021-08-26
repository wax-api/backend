from aiohttp.web import Request, Response, json_response, HTTPNotFound
from wax.component.jwt import JWTUtil
from wax.component.security import auth_user
from wax.utils import timestamp
from wax.json_util import json_dumps
from wax.mapper.user import UserMapper
from wax.wax_dsl import endpoint, Keys

@endpoint({
    'method': 'POST',
    'path': '/login',
    'description': '用户登录',
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


@endpoint({
    'method': 'GET',
    'path': '/app/me',
    'description': '查询当前登录用户信息',
    'response': {
        '200': {
            'schema': {
                'id': 'integer',
                'avatar?': 'string',
                'truename': 'string',
                'email': 'string',
                'created_at': 'string',
                'updated_at': 'string',
            }
        }
    }
})
async def me_info(request: Request) -> Response:
    user_mapper = UserMapper(request)
    user_db = await user_mapper.select_by_id(id=auth_user(request).user_id)
    if not user_db:
        raise HTTPNotFound()
    user_db -= Keys('acl')
    return json_response(user_db, dumps=json_dumps)
