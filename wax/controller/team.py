from aiohttp.web import Request


from wax.component.security import auth_user
from wax.mapper.team import TeamMapper
from wax.mapper.user import UserMapper
from wax.wax_dsl import endpoint, input_body, input_path
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
async def insert(request: Request):
    team_mapper = TeamMapper(request)
    user_mapper = UserMapper(request)
    user_id = auth_user(request).user_id
    req_data = input_body(request)
    team_id = make_unique_id()
    await team_mapper.insert(
        id=team_id, name=req_data['name'],
        read_acl=[f'T{team_id}'],
        write_acl=[f'TA{team_id}'],
    )
    await user_mapper.add_acls(id=user_id, acls=[f'T{team_id}', f'TA{team_id}'])
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
async def update(request: Request):
    team_mapper = TeamMapper(request)
    req_data = input_body(request)
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
async def delete(request: Request):
    team_mapper = TeamMapper(request)
    team_id = input_path(request)['id']
    await team_mapper.delete_by_id(id=team_id)
    return {'id': team_id}
