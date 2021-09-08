from wax.wax_dsl import endpoint
from wax.component.security import AuthUser
from wax.mapper.entity import EntityMapper
from wax.utils import make_unique_id


@endpoint({
    'method': 'GET',
    'path': '/app/entity',
    'description': '查询实体列表',
    'requestParam': {
        'query': {
            'project_id!': 'integer',
            'superset_id': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'list[]': {
                    'id': 'integer',
                    'name': 'string',
                    'superset_id': 'integer'
                }
            }
        }
    }
})
async def query_list(entity_mapper: EntityMapper, query: dict):
    entity_list = await entity_mapper.select_list(**query)
    return {'list': entity_list}


@endpoint({
    'method': 'GET',
    'path': '/app/entity/{id}',
    'description': '查询实体详情',
    'requestParam': {
        'path': {
            'id!': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': 'integer',
                'project_id': 'integer',
                'name': 'string',
                'superset_id': ['integer', '超集实体ID'],
                'content': 'string',
            }
        }
    }
})
async def query_detail(entity_mapper: EntityMapper, path: dict):
    return await entity_mapper.select_by_id(id=path['id'])


@endpoint({
    'method': 'POST',
    'path': '/app/entity',
    'description': '创建实体',
    'requestBody': {
        'schema': {
            'name!': 'string',
            'project_id!': 'integer',
            'superset_id!': ['integer', '超集实体ID'],
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '实体ID']
            }
        }
    }
})
async def insert(entity_mapper: EntityMapper, auth_user: AuthUser, body: dict):
    req_data = body['data']
    project_id = req_data['project_id']
    assert f'P{project_id}' in auth_user.acl, '无创建实体权限'
    entity_id = make_unique_id()
    await entity_mapper.insert_entity(
        id=entity_id,
        project_id=req_data['project_id'],
        superset_id=req_data['superset_id'],
        name=req_data['name'],
        content=req_data['content'],
        write_acl=[f'P{project_id}']
    )
    return {'id': entity_id}


@endpoint({
    'method': 'PUT',
    'path': '/app/entity',
    'description': '修改实体',
    'requestBody': {
        'schema': {
            'id!': 'integer',
            'name': 'string',
            'content': 'string',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '实体ID']
            }
        }
    }
})
async def update(entity_mapper: EntityMapper, body: dict):
    req_data = body['data']
    entity_id = req_data['id']
    assert await entity_mapper.writable(id=entity_id), '无修改实体权限'
    await entity_mapper.update_by_id(**req_data)
    return {'id': entity_id}


@endpoint({
    'method': 'DELETE',
    'path': '/app/entity/{id}',
    'description': '删除实体',
    'requestParam': {
        'path': {
            'id!': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '实体ID']
            }
        }
    }
})
async def delete(entity_mapper: EntityMapper, path: dict):
    entity_id = path['id']
    assert await entity_mapper.writable(id=entity_id), '无删除实体权限'
    await entity_mapper.delete_by_id(id=entity_id)
    return {'id': entity_id}
