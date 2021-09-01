from aiohttp.web import HTTPNotFound
import bcrypt
from wax.component.jwt import JWTUtil
from wax.component.security import AuthUser
from wax.utils import timestamp
from wax.mapper.user import UserMapper
from wax.mapper.auth import AuthMapper
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
async def login(user_mapper: UserMapper, jwtutil: JWTUtil, body: dict):
    req_data = body['data']
    user_db = await user_mapper.select_by_email(email=req_data['email'])
    assert user_db, 'Email不存在'
    assert bcrypt.checkpw(req_data['password'].encode(), user_db['password'].encode()), 'Email或密码错误'
    token = jwtutil.encrypt(user_db['id'], 'USER', timestamp(86400))
    return {'token': token}


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
async def me_info(user_mapper: UserMapper, auth_user: AuthUser):
    user_db = await user_mapper.select_by_id(id=auth_user.user_id)
    if not user_db:
        raise HTTPNotFound()
    user_db -= Keys('acl')
    return user_db


@endpoint({
    'method': 'PUT',
    'path': '/app/user',
    'description': '用户登录',
    'requestBody': {
        'schema': {
            'id!': ['integer', '用户ID'],
            'avatar': 'string',
            'truename': 'string',
            'email': 'string',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '用户ID']
            }
        }
    }
})
async def update(body: dict, auth_user: AuthUser, user_mapper: UserMapper):
    req_data = body['data']
    assert req_data['id'] == auth_user.user_id, '当前用户无操作权限'
    await user_mapper.update_by_id(**req_data)
    return {'id': req_data['id']}


@endpoint({
    'method': 'PUT',
    'path': '/app/user/password',
    'description': '修改密码',
    'requestBody': {
        'schema': {
            'id!': ['integer', '用户ID'],
            'password!': ['string', '新密码', {'minLength': 6}],
        }
    },
    'response': {
        '200': {
            'id': ['integer', '用户ID']
        }
    }
})
async def update_password(body: dict, auth_mapper: AuthMapper):
    req_data = body['data']
    user_id = req_data['id']
    password = bcrypt.hashpw(req_data['password'].encode(), bcrypt.gensalt()).decode()
    await auth_mapper.update_password(user_id=user_id, password=password)
    return {'id': user_id}
