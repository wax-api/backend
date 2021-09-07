from wax.wax_dsl import endpoint
from wax.component.security import AuthUser
from wax.mapper.acl import ACLMapper
from wax.mapper.project import ProjectMapper
from wax.utils import make_unique_id


@endpoint({
    'method': 'POST',
    'path': '/app/project',
    'description': '创建项目',
    'requestBody': {
        'schema': {
            'team_id!': ['integer', '所属团队ID'],
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
        project_mapper: ProjectMapper,
        aclmapper: ACLMapper,
        auth_user: AuthUser,
        body: dict):
    req_data = body['data']
    team_id = req_data['team_id']
    assert f'T{team_id}' in auth_user.acl, '无创建项目权限'
    project_id = make_unique_id()
    if req_data['visibility'] == 'public':
        project_read_acl = ['G', 'U']
    else:
        project_read_acl = [f'TA{team_id}', f'P{project_id}']
    await project_mapper.insert_project(
        id=project_id, team_id=team_id, name=req_data['name'], remark=req_data['remark'],
        read_acl=project_read_acl,
        write_acl=[f'TA{team_id}', f'PA{project_id}']
    )
    project_acl = [f'P{project_id}', f'PA{project_id}']
    await project_mapper.add_project_member(id=make_unique_id(), project_id=project_id, user_id=auth_user.user_id)
    await aclmapper.add_acls(user_id=auth_user.user_id, acls=project_acl)
    return {'id': project_id}


@endpoint({
    'method': 'PUT',
    'path': '/app/project',
    'description': '修改项目',
    'requestBody': {
        'schema': {
            'id!': ['integer', '项目ID'],
            'name': ['string', '项目名称'],
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
async def update(project_mapper: ProjectMapper, body: dict):
    req_data = body['data']
    project_id = req_data['id']
    assert await project_mapper.writable(id=project_id), '无修改项目权限'
    await project_mapper.update_by_id(**req_data)
    return {'id': project_id}


@endpoint({
    'method': 'DELETE',
    'path': '/app/project/{id}',
    'description': '删除项目',
    'requestParam': {
        'path': {
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
        aclmapper: ACLMapper,
        path: dict):
    project_id = path['id']
    assert await project_mapper.writable(id=project_id), '无删除项目权限'
    await project_mapper.delete_by_id(id=project_id)
    await project_mapper.remove_project_member(project_id=project_id)
    await aclmapper.remove_acl(acls=[f'P{project_id}'], removing_acl=f'P{project_id}')
    await aclmapper.remove_acl(acls=[f'PA{project_id}'], removing_acl=f'PA{project_id}')
    return {'id': project_id}


@endpoint({
    'method': 'GET',
    'path': '/app/project',
    'description': '查询项目列表',
    'requestParam': {
        'query': {
            'team_id!': 'integer',
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
async def query_list(project_mapper: ProjectMapper, query: dict, limit: int, offset: int):
    team_id = query['team_id']
    return await project_mapper.query_list(limit=limit, offset=offset, team_id=team_id)


@endpoint({
    'method': 'GET',
    'path': '/app/project/{id}/member',
    'description': '查询团队成员列表',
    'requestParam': {
        'path': {
            'id!': ['integer', '团队ID'],
        },
        'query': {
            'offset': 'integer',
            'limit': 'integer',
        }
    },
    'response': {
        '200': {
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
    'path': '/app/project/{id}/member',
    'description': '添加或编辑项目成员',
    'requestParam': {
        'path': {
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
async def save_member(project_mapper: ProjectMapper, aclmapper: ACLMapper, path: dict, body: dict):
    req_data = body['body']
    project_id = path['id']
    user_id = req_data['user_id']
    role = req_data['role']
    assert await project_mapper.writable(id=project_id), '无编辑项目成员权限'
    role_db = await project_mapper.select_project_role(project_id=project_id, user_id=user_id)
    if role_db:  # 编辑项目成员
        await project_mapper.update_project_member(project_id=project_id, user_id=user_id, role=role)
        removing_acl = {'admin': f'PA{project_id}', 'member': f'P{project_id}'}[role_db['role']]
        await aclmapper.remove_acl([f'U{user_id}'], removing_acl=removing_acl)
    else:  # 添加项目成员
        await project_mapper.add_project_member(id=make_unique_id(), project_id=project_id, user_id=user_id, role=role)
    if role == 'admin':
        await aclmapper.add_acls(user_id=user_id, acls=[f'PA{project_id}', f'P{project_id}'])
    else:
        await aclmapper.add_acls(user_id=user_id, acls=[f'P{project_id}'])
    # todo 同步directory, entity, interface, mock的read_acl和write_acl
    return {'id': project_id}


@endpoint({
    'method': 'DELETE',
    'path': '/app/project/{id}/member',
    'description': '移除项目成员',
    'requestParam': {
        'path': {
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
async def remove_member(project_mapper: ProjectMapper, aclmapper: ACLMapper, path: dict, query: dict):
    project_id = path['id']
    user_id = query['user_id']
    assert await project_mapper.writable(id=project_id), '无移除项目成员权限'
    await project_mapper.remove_project_member(project_id=project_id, user_id=user_id)
    await aclmapper.remove_acl([f'U{user_id}'], removing_acl=f'PA{project_id}')
    await aclmapper.remove_acl([f'U{user_id}'], removing_acl=f'P{project_id}')
    return {'id': project_id}

