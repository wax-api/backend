from wax.component.security import AuthUser
from wax.mapper.team import TeamMapper
from wax.mapper.acl import ACLMapper
from wax.wax_dsl import endpoint
from wax.utils import make_unique_id, eafp


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
    assert await team_mapper.insert_team(
        id=team_id, name=req_data['name'],
        read_acl=[f'T{team_id}'],
        write_acl=[f'TA{team_id}'],
    ) > 0, '创建团队失败，或无权限操作'
    team_acl = [f'T{team_id}', f'TA{team_id}']
    auth_user.acl.extend(team_acl)
    assert await team_mapper.add_team_member(
        id=make_unique_id(), team_id=team_id, user_id=auth_user.user_id) > 0, '添加团队成员失败'
    await aclmapper.add_acls(user_id=auth_user.user_id, acls=team_acl)
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
            'schema': {
                'id': ['integer', '团队ID']
            }
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
    await team_mapper.remove_team_member(team_id=team_id)  # 必须先删关系，再删团队，不然acl有问题
    await team_mapper.delete_by_id(id=team_id)
    await aclmapper.remove_acl(acls=[f'T{team_id}', f'TA{team_id}'], removing_acl=f'T{team_id}')
    await aclmapper.remove_acl(acls=[f'T{team_id}', f'TA{team_id}'], removing_acl=f'TA{team_id}')
    return {'id': team_id}


@endpoint({
    'method': 'DELETE',
    'path': '/app/team/{id}/member',
    'description': '删除团队成员',
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
            'id': ['integer', '用户ID']
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
    await team_mapper.remove_team_member(team_id=team_id, user_id=user_id)
    await aclmapper.remove_acl(acls=[f'U{user_id}'], removing_acl=f'T{team_id}')
    await aclmapper.remove_acl(acls=[f'U{user_id}'], removing_acl=f'TA{team_id}')
    return {'id': user_id}


@endpoint({
    'method': 'GET',
    'path': '/app/team/{id}/member',
    'description': '查询团队成员列表',
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
                'limit': 'integer',
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
