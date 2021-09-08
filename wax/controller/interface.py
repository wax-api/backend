from wax.wax_dsl import endpoint
from wax.component.security import AuthUser
from wax.mapper.interface import InterfaceMapper
from wax.mapper.directory import DirectoryMapper
from wax.utils import make_unique_id


@endpoint({
    'method': 'GET',
    'path': '/app/interface',
    'description': '查询接口列表',
    'requestParam': {
        'query': {
            'project_id!': 'integer',
            'directory_id': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'list[]': {
                    'id': 'integer',
                    'name': 'string',
                    'method': 'string',
                    'path': 'string',
                    'directory_id': 'integer',
                }
            }
        }
    }
})
async def query_list(interface_mapper: InterfaceMapper, query: dict):
    interface_list = await interface_mapper.select_list(project_id=query['project_id'], directory_id=query.get('directory_id'))
    return {'list': interface_list}


@endpoint({
    'method': 'GET',
    'path': '/app/interface/{id}',
    'description': '查询接口详情',
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
                'method': 'string',
                'path': 'string',
                'directory_id': 'integer',
                'status': ['string', {'enum': ['active', 'closed']}],
                'created_at': 'string',
                'create_user_id': 'integer',
                'updated_at': 'string',
                'update_user_id': 'integer',
                'endpoint': 'string',
            }
        }
    }
})
async def query_detail(interface_mapper: InterfaceMapper, path: dict):
    return await interface_mapper.select_by_id(id=path['id'])


@endpoint({
    'method': 'POST',
    'path': '/app/interface',
    'description': '创建接口',
    'requestBody': {
        'schema': {
            'project_id!': 'integer',
            'directory_id!': 'integer',
            'name': 'string',
            'method': 'string',
            'path': 'string',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '接口ID']
            }
        }
    }
})
async def insert(
        interface_mapper: InterfaceMapper,
        directory_mapper: DirectoryMapper,
        auth_user: AuthUser,
        body: dict):
    req_data = body['data']
    project_id = req_data['project_id']
    directory_id = req_data['directory_id']
    assert f'P{project_id}' in auth_user.acl, '无创建接口分类权限'
    assert (directory_db := await directory_mapper.select_by_id(id=directory_id)) and \
       directory_db.get('project_id', 0) == directory_id, '接口分类ID参数错误'
    interface_id = make_unique_id()
    await interface_mapper.insert_interface(
        id=interface_id,
        project_id=req_data['project_id'],
        directory_id=req_data['directory_id'],
        name=req_data['name'],
        method=req_data['method'],
        path=req_data['path'],
        write_acl=[f'P{project_id}']
    )
    return {'id': interface_id}


@endpoint({
    'method': 'DELETE',
    'path': '/app/interface/{id}',
    'description': '删除接口',
    'requestParam': {
        'path': {
            'id!': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '接口ID']
            }
        }
    }
})
async def delete(interface_mapper: InterfaceMapper, path: dict):
    interface_id = path['id']
    await interface_mapper.delete_by_id(id=interface_id)
    return {'id': interface_id}


@endpoint({
    'method': 'PUT',
    'path': '/app/interface',
    'description': '修改接口分类',
    'requestBody': {
        'schema': {
            'id!': 'integer',
            'name': 'string',
            'method': 'string',
            'path': 'string',
            'directory_id': 'integer',
            'status': ['string', {'enum': ['active', 'closed']}],
            'endpoint': 'string',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '接口ID']
            }
        }
    }
})
async def update(interface_mapper: InterfaceMapper, body: dict):
    req_data = body['data']
    interface_id = req_data['id']
    assert await interface_mapper.writable(id=interface_id), '无修改接口分类权限'
    await interface_mapper.update_by_id(**req_data)
