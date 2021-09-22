import asyncio
from wax.wax_dsl import endpoint
from wax.component.gateway import Gateway
from wax.component.security import AuthUser
from wax.mapper.project import ProjectMapper
from wax.utils import make_unique_id


@endpoint({
    'method': 'POST',
    'path': '/app/team/{team_id}/project',
    'summary': '创建项目',
    'requestParam': {
        'path': {
            'team_id!': ['integer', '团队ID'],
        }
    },
    'requestBody': {
        'schema': {
            'name!': ['string', '项目名称'],
            'remark': ['string', '项目描述'],
            'visibility!': ['string', '可见度', {'enum': ['public', 'private']}]
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '项目ID']
            }
        }
    }
})
async def create(
        gateway: Gateway,
        project_mapper: ProjectMapper,
        auth_user: AuthUser,
        body: dict,
        path: dict):
    req_data = body['data']
    team_id = path['team_id']
    project_id = make_unique_id()
    await project_mapper.insert_project(id=project_id, team_id=team_id, name=req_data['name'], remark=req_data['remark'])
    await project_mapper.add_project_member(id=make_unique_id(), project_id=project_id, user_id=auth_user.user_id)
    await asyncio.gather(
        gateway.put_user_acl(user_id=auth_user.user_id, add_acls=[f'P/{project_id}', f'PA/{project_id}']),
        gateway.put_api_acl(method='PUT', path=f'/app/team/{team_id}/project/{project_id}', add_acls=[f'PA/{project_id}', f'TA/{team_id}']),
        gateway.put_api_acl(method='DELETE', path=f'/app/team/{team_id}/project/{project_id}', add_acls=[f'PA/{project_id}', f'TA/{team_id}']),
        gateway.put_api_acl(method='GET', path=f'/app/team/{team_id}/project/{project_id}/member', add_acls=[f'P/{project_id}', f'TA/{team_id}']),
        gateway.put_api_acl(method='PUT', path=f'/app/team/{team_id}/project/{project_id}/member', add_acls=[f'PA/{project_id}', f'TA/{team_id}']),
        gateway.put_api_acl(method='DELETE', path=f'/app/team/{team_id}/project/{project_id}/member', add_acls=[f'PA/{project_id}', f'TA/{team_id}']),
        gateway.put_api_acl(method='GET', path=f'/app/project/{project_id}/directory', add_acls=[f'P/{project_id}', f'TA/{team_id}']),
        gateway.put_api_acl(method='POST', path=f'/app/project/{project_id}/directory', add_acls=[f'P/{project_id}', f'TA/{team_id}']),
        gateway.put_api_acl(method='GET', path=f'/app/project/{project_id}/interface', add_acls=[f'P/{project_id}', f'TA/{team_id}']),
        gateway.put_api_acl(method='POST', path=f'/app/project/{project_id}/interface', add_acls=[f'P/{project_id}', f'TA/{team_id}']),
        gateway.put_api_acl(method='GET', path=f'/app/project/{project_id}/entity', add_acls=[f'P/{project_id}', f'TA/{team_id}']),
        gateway.put_api_acl(method='POST', path=f'/app/project/{project_id}/entity', add_acls=[f'P/{project_id}', f'TA/{team_id}']),
        gateway.put_api_acl(method='GET', path=f'/app/project/{project_id}/mock', add_acls=[f'P/{project_id}', f'TA/{team_id}']),
        gateway.put_api_acl(method='POST', path=f'/app/project/{project_id}/mock', add_acls=[f'P/{project_id}', f'TA/{team_id}']),
    )
    return {'id': project_id}


@endpoint({
    'method': 'PUT',
    'path': '/app/team/{team_id}/project/{id}',
    'summary': '修改项目',
    'requestParam': {
        'path': {
            'team_id!': ['integer', '团队ID'],
            'id!': ['integer', '项目ID'],
        }
    },
    'requestBody': {
        'schema': {
            'name': ['string', '项目名称'],
            'remark': ['string', '项目描述'],
            'visibility': ['string', '可见度', {'enum': ['public', 'private']}]
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '项目ID']
            }
        }
    }
})
async def update(project_mapper: ProjectMapper, body: dict, path: dict):
    req_data = body['data']
    project_id = path['id']
    await project_mapper.update_by_id(id=project_id, **req_data)
    return {'id': project_id}


@endpoint({
    'method': 'DELETE',
    'path': '/app/team/{team_id}/project/{id}',
    'summary': '删除项目',
    'requestParam': {
        'path': {
            'team_id!': ['integer', '团队ID'],
            'id!': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '项目ID']
            }
        }
    }
})
async def delete(
        project_mapper: ProjectMapper,
        path: dict):
    project_id = path['id']
    await project_mapper.delete_by_id(id=project_id)
    await project_mapper.remove_project_member(project_id=project_id)
    return {'id': project_id}


@endpoint({
    'method': 'GET',
    'path': '/app/team/{team_id}/project',
    'summary': '查询项目列表',
    'requestParam': {
        'path': {
            'team_id!': ['integer', '团队ID'],
        },
        'query': {
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
                    'id': ['integer', '项目ID'],
                    'name': ['string', '项目名称'],
                    'remark': ['string', '项目描述'],
                    'visibility': ['string', '可见度', {'enum': ['public', 'private']}]
                }
            }
        }
    }
})
async def query_list(project_mapper: ProjectMapper, path: dict, limit: int, offset: int):
    team_id = path['team_id']
    return await project_mapper.query_list(limit=limit, offset=offset, team_id=team_id)


@endpoint({
    'method': 'GET',
    'path': '/app/team/{team_id}/project/{id}/member',
    'summary': '查询项目成员列表',
    'requestParam': {
        'path': {
            'team_id!': ['integer', '团队ID'],
            'id!': ['integer', '项目ID'],
        },
        'query': {
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
                    'project_role?': ['string', {'enum': ['admin', 'member']}]
                }
            }
        }
    }
})
async def list_member(
        project_mapper: ProjectMapper,
        path: dict,
        limit: int,
        offset: int):
    project_id = path['id']
    return await project_mapper.query_member_list(limit=limit, offset=offset, project_id=project_id)


@endpoint({
    'method': 'PUT',
    'path': '/app/team/{team_id}/project/{id}/member',
    'summary': '添加或编辑项目成员',
    'requestParam': {
        'path': {
            'team_id!': ['integer', '团队ID'],
            'id!': 'integer',
        }
    },
    'requestBody': {
        'schema': {
            'user_id!': ['integer', '用户ID'],
            'role!': ['string', '成员角色', {'enum': ['admin', 'member']}],
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '项目ID']
            }
        }
    }
})
async def save_member(project_mapper: ProjectMapper, path: dict, body: dict):
    req_data = body['body']
    project_id = path['id']
    user_id = req_data['user_id']
    role = req_data['role']
    try:  # 添加项目成员
        await project_mapper.add_project_member(id=make_unique_id(), project_id=project_id, user_id=user_id, role=role)
    except:  # 编辑项目成员
        await project_mapper.update_project_member(project_id=project_id, user_id=user_id, role=role)
    return {'id': project_id}


@endpoint({
    'method': 'DELETE',
    'path': '/app/team/{team_id}/project/{id}/member',
    'summary': '移除项目成员',
    'requestParam': {
        'path': {
            'team_id!': ['integer', '团队ID'],
            'id!': 'integer',
        },
        'query': {
            'user_id!': ['integer', '用户ID'],
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '项目ID']
            }
        }
    }
})
async def remove_member(project_mapper: ProjectMapper, path: dict, query: dict):
    project_id = path['id']
    user_id = query['user_id']
    await project_mapper.remove_project_member(project_id=project_id, user_id=user_id)
    return {'id': project_id}
