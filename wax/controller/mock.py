from wax.wax_dsl import endpoint
from wax.mapper.mock import MockMapper
from wax.utils import make_unique_id


@endpoint({
    'method': 'GET',
    'path': '/app/project/{project_id}/mock',
    'summary': '查询mock列表',
    'requestParam': {
        'path': {
            'project_id': 'integer',
        },
        'query': {
            'interface_iid!': 'integer',
            'status_code': 'string',
        }
    },
    'response': {
        '200': {
            'schema': {
                'list[]': {
                    'id': 'integer',
                    'name': 'string',
                    'interface_iid!': 'integer',
                    'status_code!': 'string',
                    'content_type': 'string',
                    'active': 'integer',
                }
            }
        }
    }
})
async def query_list(mock_mapper: MockMapper, path: dict, query: dict):
    project_id = path['project_id']
    mock_list = await mock_mapper.select_list(project_id=project_id, **query)
    return {'list': mock_list}


@endpoint({
    'method': 'GET',
    'path': '/app/project/{project_id}/mock/{id}',
    'summary': '查询mock详情',
    'requestParam': {
        'path': {
            'project_id!': 'integer',
            'id!': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': 'integer',
                'name': 'string',
                'interface_iid!': 'integer',
                'status_code!': 'string',
                'content_type': 'string',
                'mockjs': 'string',
                'content': 'string',
                'type': ['mock类型', {'enum': ['mockjs', 'json']}],
                'headers': 'string',
                'active': 'integer',
            }
        }
    }
})
async def query_detail(mock_mapper: MockMapper, path: dict):
    return await mock_mapper.select_by_id(id=path['id'])


@endpoint({
    'method': 'POST',
    'path': '/app/project/{project_id}/mock',
    'summary': '创建mock',
    'requestParam': {
        'path': {
            'project_id!': 'integer',
        }
    },
    'requestBody': {
        'schema': {
            'name!': 'string',
            'interface_iid!': 'integer',
            'status_code!': 'string',
            'content_type!': 'string',
            'mockjs!': 'string',
            'content!': 'string',
            'type!': ['mock类型', {'enum': ['mockjs', 'json']}],
            'headers!': 'string',
            'active!': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', 'mock ID']
            }
        }
    }
})
async def insert(mock_mapper: MockMapper, path: dict, body: dict):
    req_data = body['data']
    project_id = path['project_id']
    interface_iid = req_data['interface_iid']
    mock_id = make_unique_id()
    if req_data['active']:
        await mock_mapper.unactive_all(project_id=project_id, interface_iid=interface_iid)
    await mock_mapper.insert_mock(id=mock_id, **req_data)


@endpoint({
    'method': 'PUT',
    'path': '/app/project/{project_id}/mock/{id}',
    'summary': '修改mock',
    'requestParam': {
        'path': {
            'id!': 'integer',
            'project_id!': 'integer',
        }
    },
    'requestBody': {
        'schema': {
            'name': 'string',
            'status_code!': 'string',
            'content_type': 'string',
            'mockjs': 'string',
            'content': 'string',
            'type': ['mock类型', {'enum': ['mockjs', 'json']}],
            'headers': 'string',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', 'mock ID']
            }
        }
    }
})
async def update(mock_mapper: MockMapper, path: dict, body: dict):
    req_data = body['data']
    mock_id = path['id']
    await mock_mapper.update_by_id(id=mock_id, **req_data)
    return {'id': mock_id}


@endpoint({
    'method': 'DELETE',
    'path': '/app/project/{project_id}/mock/{id}',
    'summary': '删除mock',
    'requestParam': {
        'path': {
            'project_id!': 'integer',
            'id!': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', 'mock ID']
            }
        }
    }
})
async def delete(mock_mapper: MockMapper, path: dict):
    mock_id = path['id']
    await mock_mapper.delete_by_id(id=mock_id)
    return {'id': mock_id}


@endpoint({
    'method': 'PUT',
    'path': '/app/project/{project_id}/mock/{id}/active',
    'summary': '设置生效mock',
    'requestParam': {
        'path': {
            'project_id!': 'integer',
            'id!': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', 'mock ID']
            }
        }
    }
})
async def active(mock_mapper: MockMapper, path: dict):
    mock_id = path['id']
    assert (mock_db := await mock_mapper.select_by_id(id=mock_id)), "Mock ID不存在"
    await mock_mapper.unactive_all(project_id=mock_db['project_id'], interface_iid=mock_db['interface_iid'])
    await mock_mapper.update_by_id(id=mock_id, active=1)
    return {'id': mock_id}
