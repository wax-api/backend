from wax.component.security import AuthUser
from wax.mapper.team import TeamMapper
from wax.mapper.user import UserMapper
from wax.wax_dsl import endpoint
from wax.utils import make_unique_id


@endpoint({
    'method': 'POST',
    'path': '/app/team',
    'description': '创建团队',
    'requestBody': {
        'schema': {
            'name!': ['string', '团队名称', {'minLength': 2}],
        }
    },
    'response': {
        '200': {
            'id': ['integer', '团队ID']
        }
    }
})
async def insert(team_mapper: TeamMapper, user_mapper: UserMapper, auth_user: AuthUser, body: dict):
    req_data = body['data']
    team_id = make_unique_id()
    await team_mapper.insert(
        id=team_id, name=req_data['name'],
        read_acl=[f'T{team_id}'],
        write_acl=[f'TA{team_id}'],
    )
    await user_mapper.add_acls(id=auth_user.user_id, acls=[f'T{team_id}', f'TA{team_id}'])
    return {'id': team_id}


@endpoint({
    'method': 'PUT',
    'path': '/app/team',
    'description': '修改团队',
    'requestBody': {
        'schema': {
            'id!': 'integer',
            'name': ['string', '团队名称', {'minLength': 2}],
        }
    },
    'response': {
        '200': {
            'id': ['integer', '团队ID']
        }
    }
})
async def update(team_mapper: TeamMapper, body: dict):
    req_data = body['data']
    await team_mapper.update_by_id(id=req_data['id'], name=req_data['name'])
    return {'id': req_data['id']}


@endpoint({
    'method': 'DELETE',
    'path': '/app/team/{id}',
    'description': '删除团队',
    'requestParam': {
        'path': {
            'id!': ['integer', '团队ID']
        }
    },
    'response': {
        '200': {
            'id': ['integer', '团队ID']
        }
    }
})
async def delete(team_mapper: TeamMapper, path: dict):
    team_id = path['id']
    await team_mapper.delete_by_id(id=team_id)
    return {'id': team_id}
