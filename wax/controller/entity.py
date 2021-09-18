from wax.wax_dsl import endpoint
from wax.mapper.entity import EntityMapper
from wax.utils import make_unique_id


@endpoint({
    'method': 'GET',
    'path': '/app/project/{project_id}/entity',
    'summary': '查询实体列表',
    'requestParam': {
        'path': {
            'project_id!': 'integer',
        },
        'query': {
            'superset_iid': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'list[]': {
                    'id': 'integer',
                    'name': 'string',
                    'superset_id': 'integer',
                    'superset_iid': 'integer',
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
    'summary': '查询实体详情',
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
    'path': '/app/project/{project_id}/entity',
    'summary': '创建实体',
    'requestParam': {
        'path': {
            'project_id!': 'integer',
        }
    },
    'requestBody': {
        'schema': {
            'name!': 'string',
            'superset_iid!': ['integer', '超集实体IID'],
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '实体ID'],
                'iid': ['integer', '实体IID'],
            }
        }
    }
})
async def insert(entity_mapper: EntityMapper, path: dict, body: dict):
    req_data = body['data']
    project_id = path['project_id']
    entity_id = make_unique_id()
    await entity_mapper.insert_entity(
        id=entity_id,
        project_id=project_id,
        **req_data
    )
    return {'id': entity_id}


@endpoint({
    'method': 'PUT',
    'path': '/app/entity/{id}',
    'summary': '修改实体',
    'requestParam': {
        'path': {
            'id!': 'integer',
        }
    },
    'requestBody': {
        'schema': {
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
async def update(entity_mapper: EntityMapper, path: dict, body: dict):
    req_data = body['data']
    entity_id = path['id']
    await entity_mapper.update_by_id(id=entity_id, **req_data)
    return {'id': entity_id}


@endpoint({
    'method': 'DELETE',
    'path': '/app/entity/{id}',
    'summary': '删除实体',
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
    await entity_mapper.delete_by_id(id=entity_id)
    return {'id': entity_id}
