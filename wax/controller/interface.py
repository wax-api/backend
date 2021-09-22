from wax.wax_dsl import endpoint
from wax.mapper.interface import InterfaceMapper
from wax.utils import make_unique_id


@endpoint({
    'method': 'GET',
    'path': '/app/project/{project_id}/interface',
    'summary': '查询接口列表',
    'requestParam': {
        'path': {
            'project_id!': 'integer',
        },
        'query': {
            'directory_iid': 'integer',
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
                    'directory_iid': 'integer',
                }
            }
        }
    }
})
async def query_list(interface_mapper: InterfaceMapper, path: dict, query: dict):
    interface_list = await interface_mapper.select_list(project_id=path['project_id'], directory_iid=query.get('directory_iid'))
    return {'list': interface_list}


@endpoint({
    'method': 'GET',
    'path': '/app/interface/{id}',
    'summary': '查询接口详情',
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
    'path': '/app/project/{project_id}/interface',
    'summary': '创建接口',
    'requestParam': {
        'path': {
            'project_id!': 'integer',
        }
    },
    'requestBody': {
        'schema': {
            'directory_iid!': 'integer',
            'name!': 'string',
            'method!': 'string',
            'path!': 'string',
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
        path: dict,
        body: dict):
    req_data = body['data']
    project_id = path['project_id']
    interface_id = make_unique_id()
    await interface_mapper.insert_interface(
        id=interface_id,
        iid=interface_id,
        project_id=project_id,
        **req_data,
    )
    return {'id': interface_id}


@endpoint({
    'method': 'DELETE',
    'path': '/app/project/{project_id}/interface/{id}',
    'summary': '删除接口',
    'requestParam': {
        'path': {
            'project_id!': 'integer',
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
    'path': '/app/interface/{id}',
    'summary': '修改接口分类',
    'requestParam': {
        'path': {
            'id!': 'integer',
        }
    },
    'requestBody': {
        'schema': {
            'name': 'string',
            'method': 'string',
            'path': 'string',
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
async def update(interface_mapper: InterfaceMapper, path: dict, body: dict):
    req_data = body['data']
    interface_id = path['id']
    await interface_mapper.update_by_id(id=interface_id, **req_data)
    return {'id': interface_id}


@endpoint({
    'method': 'PUT',
    'path': '/app/interface/{id}/directory',
    'summary': '修改接口分类',
    'requestParam': {
        'path': {
            'id!': 'integer',
        }
    },
    'requestBody': {
        'schema': {
            'directory_iid!': 'integer',
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
async def update_directory(
        interface_mapper: InterfaceMapper,
        path: dict,
        body: dict):
    req_data = body['data']
    interface_id = path['id']
    directory_iid = req_data['directory_iid']
    await interface_mapper.update_by_id(id=interface_id, directory_iid=directory_iid)
    return {'id': interface_id}
