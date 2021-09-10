from wax.wax_dsl import endpoint
from wax.component.security import AuthUser
from wax.mapper.mock import MockMapper
from wax.utils import make_unique_id


@endpoint({
    'method': 'GET',
    'path': '/app/mock',
    'summary': '查询mock列表',
    'requestParam': {
        'query': {
            'interface_id!': 'integer',
            'status_code': 'string',
        }
    },
    'response': {
        '200': {
            'schema': {
                'list[]': {
                    'id': 'integer',
                    'name': 'string',
                    'interface_id!': 'integer',
                    'status_code!': 'string',
                    'content_type': 'string',
                    'active': 'integer',
                }
            }
        }
    }
})
async def query_list(mock_mapper: MockMapper, query: dict):
    mock_list = await mock_mapper.select_list(**query)
    return {'list': mock_list}


@endpoint({
    'method': 'GET',
    'path': '/app/mock/{id}',
    'summary': '查询mock详情',
    'requestParam': {
        'path': {
            'id!': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': 'integer',
                'name': 'string',
                'interface_id!': 'integer',
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
    'path': '/app/mock',
    'summary': '创建mock',
    'requestBody': {
        'schema': {
            'name!': 'string',
            'project_id!': 'integer',
            'interface_id!': 'integer',
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
async def insert(mock_mapper: MockMapper,  auth_user: AuthUser, body: dict):
    req_data = body['data']
    project_id = req_data['project_id']
    assert f'P{project_id}' in auth_user.acl, '无创建mock权限'
    mock_id = make_unique_id()
    if req_data['active']:
        await mock_mapper.unactive_except(id=mock_id, interface_id=req_data['interface_id'])
    await mock_mapper.insert_mock(id=mock_id, write_acl=[f'P{project_id}'], **req_data)


@endpoint({
    'method': 'PUT',
    'path': '/app/mock',
    'summary': '修改mock',
    'requestBody': {
        'schema': {
            'id!': 'integer',
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
async def update(mock_mapper: MockMapper, body: dict):
    req_data = body['data']
    mock_id = req_data['id']
    assert await mock_mapper.writable(id=mock_id), '无修改mock权限'
    await mock_mapper.update_by_id(**req_data)
    return {'id': mock_id}


@endpoint({
    'method': 'DELETE',
    'path': '/app/mock/{id}',
    'summary': '删除mock',
    'requestParam': {
        'path': {
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
    assert await mock_mapper.writable(id=mock_id), '无删除mock权限'
    await mock_mapper.delete_by_id(id=mock_id)
    return {'id': mock_id}


@endpoint({
    'method': 'PUT',
    'path': '/app/mock/{id}/active',
    'summary': '设置生效mock',
    'requestParam': {
        'path': {
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
    assert (mock_db := await mock_mapper.writable(id=mock_id)), '无设置mock权限'
    await mock_mapper.unactive_except(id=mock_id, interface_id=mock_db['interface_id'])
    await mock_mapper.update_by_id(id=mock_id, active=1)
    return {'id': mock_id}
