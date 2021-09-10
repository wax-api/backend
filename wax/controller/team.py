from wax.component.security import AuthUser
from wax.mapper.team import TeamMapper
from wax.mapper.acl import ACLMapper
from wax.wax_dsl import endpoint
from wax.utils import make_unique_id, eafp


@endpoint({
    'method': 'POST',
    'path': '/app/team',
    'summary': '创建团队',
    'requestBody': {
        'schema': {
            'name!': ['string', '团队名称', {'minLength': 2}],
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '团队ID']
            }
        }
    }
})
async def insert(
        team_mapper: TeamMapper,
        aclmapper: ACLMapper,
        auth_user: AuthUser,
        body: dict):
    req_data = body['data']
    team_id = make_unique_id()
    assert await team_mapper.writable(id=team_id), '无创建团队权限'
    await team_mapper.insert_team(
        id=team_id, name=req_data['name'],
        read_acl=[f'T{team_id}'],
        write_acl=[f'TA{team_id}'],
    )
    team_acl = [f'T{team_id}', f'TA{team_id}']
    await team_mapper.add_team_member(id=make_unique_id(), team_id=team_id, user_id=auth_user.user_id)
    await aclmapper.add_acls(user_id=auth_user.user_id, acls=team_acl)
    return {'id': team_id}


@endpoint({
    'method': 'PUT',
    'path': '/app/team',
    'summary': '修改团队',
    'requestBody': {
        'schema': {
            'id!': 'integer',
            'name': ['string', '团队名称', {'minLength': 2}],
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '团队ID']
            }
        }
    }
})
async def update(team_mapper: TeamMapper, body: dict):
    req_data = body['data']
    team_id = req_data['id']
    assert await team_mapper.writable(id=team_id), '无修改团队权限'
    await team_mapper.update_by_id(id=team_id, name=req_data['name'])
    return {'id': req_data['id']}


@endpoint({
    'method': 'DELETE',
    'path': '/app/team/{id}',
    'summary': '删除团队',
    'requestParam': {
        'path': {
            'id!': ['integer', '团队ID']
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '团队ID']
            }
        }
    }
})
async def delete(
        team_mapper: TeamMapper,
        aclmapper: ACLMapper,
        path: dict):
    team_id = path['id']
    assert await team_mapper.writable(id=team_id), '无删除团队权限'
    await team_mapper.remove_team_member(team_id=team_id)
    await team_mapper.delete_by_id(id=team_id)
    await aclmapper.remove_acl(acls=[f'T{team_id}'], removing_acl=f'T{team_id}')
    await aclmapper.remove_acl(acls=[f'TA{team_id}'], removing_acl=f'TA{team_id}')
    return {'id': team_id}


@endpoint({
    'method': 'DELETE',
    'path': '/app/team/{id}/member',
    'summary': '删除团队成员',
    'requestParam': {
        'path': {
            'id!': 'integer',
        },
        'query': {
            'user_id!': 'integer',
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
async def remove_member(
        team_mapper: TeamMapper,
        aclmapper: ACLMapper,
        path: dict,
        query: dict):
    team_id = path['id']
    user_id = query['user_id']
    assert await team_mapper.writable(id=team_id), '无删除团队成员权限'
    await team_mapper.remove_team_member(team_id=team_id, user_id=user_id)
    await aclmapper.remove_acl(acls=[f'U{user_id}'], removing_acl=f'T{team_id}')
    await aclmapper.remove_acl(acls=[f'U{user_id}'], removing_acl=f'TA{team_id}')
    return {'id': user_id}


@endpoint({
    'method': 'GET',
    'path': '/app/team/{id}/member',
    'summary': '查询团队成员列表',
    'requestParam': {
        'path': {
            'id!': 'integer',
        },
        'query': {
            'keyword': 'string',
            'project_id': 'integer',
            'offset': 'integer',
            'limit': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'total': 'integer',
                'offset': 'integer',
                'list[]': {
                    'id': ['integer', '用户ID'],
                    'avatar?': 'string',
                    'truename': 'string',
                    'email': 'string',
                    'team_id': 'integer',
                    'created_at': 'string',
                    'updated_at': 'string',
                    'team_role': ['string', {'enum': ['admin', 'member']}],
                    'project_role?': ['string', {'enum': ['admin', 'member']}]
                }
            }
        }
    }
})
async def list_member(team_mapper: TeamMapper, path: dict, query: dict, offset: int, limit: int):
    team_id = path['team_id']
    keyword = eafp(lambda: '%' + query['keyword'] + '%')
    project_id = query.get('project_id')
    return await team_mapper.select_team_member(offset=offset, limit=limit, team_id=team_id, keyword=keyword, project_id=project_id)
