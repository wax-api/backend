from aiohttp.web import HTTPNotFound
import bcrypt
from wax.component.jwt import JWTUtil
from wax.component.security import AuthUser
from wax.component.gateway import Gateway
from wax.utils import timestamp, make_unique_id
from wax.mapper.user import UserMapper
from wax.mapper.auth import AuthMapper
from wax.mapper.team import TeamMapper
from wax.wax_dsl import endpoint


@endpoint({
    'method': 'POST',
    'path': '/login',
    'summary': '用户登录',
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
async def login(user_mapper: UserMapper, auth_mapper: AuthMapper, jwtutil: JWTUtil, body: dict):
    req_data = body['data']
    user_db = await user_mapper.select_by_email(email=req_data['email'])
    assert user_db, 'Email不存在'
    auth_db = await auth_mapper.select_by_user_id(user_id=user_db['id'])
    assert auth_db, '无法登录，联系管理员'
    assert bcrypt.checkpw(req_data['password'].encode(), auth_db['password'].encode()), 'Email或密码错误'
    token = jwtutil.encrypt(user_db['id'], 'USER', timestamp(86400))
    return {'token': token}


@endpoint({
    'method': 'GET',
    'path': '/app/me',
    'summary': '查询当前登录用户信息',
    'response': {
        '200': {
            'schema': {
                'id': 'integer',
                'avatar?': 'string',
                'truename': 'string',
                'email': 'string',
                'team_id': 'integer',
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
    return user_db


@endpoint({
    'method': 'PUT',
    'path': '/app/user/{id}',
    'summary': '编辑用户信息',
    'requestParam': {
        'path': {
            'id!': ['integer', '用户ID'],
        }
    },
    'requestBody': {
        'schema': {
            'avatar': ['string', '用户头像链接'],
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
async def update(user_mapper: UserMapper, body: dict, path: dict):
    user_id = path['id']
    req_data = body['data']
    assert await user_mapper.writable(id=user_id), '编辑用户失败'
    await user_mapper.update_by_id(id=user_id, **req_data)
    return {'id': user_id}


@endpoint({
    'method': 'PUT',
    'path': '/app/user/{id}/password',
    'summary': '修改密码',
    'requestParam': {
        'path': {
            'id!': 'integer',
        }
    },
    'requestBody': {
        'schema': {
            'password!': ['string', '新密码', {'minLength': 6}],
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '用户ID']
            },
        }
    }
})
async def update_password(auth_mapper: AuthMapper, body: dict, path: dict):
    req_data = body['data']
    user_id = path['id']
    assert await auth_mapper.writable(user_id=user_id), '修改密码失败'
    password = bcrypt.hashpw(req_data['password'].encode(), bcrypt.gensalt()).decode()
    await auth_mapper.update_password(user_id=user_id, password=password)
    return {'id': user_id}


@endpoint({
    'method': 'POST',
    'path': '/app/team/{id}/user',
    'summary': '创建用户',
    'requestParam': {
        'path': {
            'id!': ['integer', '团队ID'],
        }
    },
    'requestBody': {
        'schema': {
            'truename!': 'string',
            'email!': 'string',
            'password!': ['string', '初始密码', {'minLength': 6}],
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '用户ID']
            },
        }
    }
})
async def create_user(
        user_mapper: UserMapper,
        auth_mapper: AuthMapper,
        team_mapper: TeamMapper,
        gateway: Gateway,
        body: dict,
        path: dict):
    team_id = path['id']
    req_data = body['data']
    # 创建用户
    user_id = make_unique_id()
    await user_mapper.insert_user(
        id=user_id,
        truename=req_data['truename'],
        email=req_data['email'],
        team_id=team_id,
    )
    await auth_mapper.insert_auth(
        user_id=user_id,
        password=req_data['password'],
    )
    # 添加团队关系
    await team_mapper.add_team_member(id=make_unique_id(), team_id=team_id, user_id=user_id)
    # 添加User ACL
    await gateway.put_user_acl(user_id=user_id, add_acls=[f'U/{user_id}', f'T/{team_id}'])
    # 添加API ACL
    await gateway.put_api_acl(method='PUT', path=f'/app/user/{user_id}', add_acls=[f'U/{user_id}'])
    await gateway.put_api_acl(method='PUT', path=f'/app/user/{user_id}/password', add_acls=[f'U/{user_id}'])
    return {'id': user_id}
