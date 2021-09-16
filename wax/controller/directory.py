from wax.wax_dsl import endpoint
from wax.mapper.directory import DirectoryMapper
from wax.utils import make_unique_id


@endpoint({
    'method': 'GET',
    'path': '/app/project/{project_id}/directory',
    'summary': '查询分类列表',
    'requestParam': {
        'path': {
            'project_id!': ['integer', '项目ID'],
        }
    },
    'response': {
        '200': {
            'schema': {
                'list[]': {
                    'id': 'integer',
                    'name': 'string',
                    'parent': 'integer',
                }
            }
        }
    }
})
async def query_list(directory_mapper: DirectoryMapper, path: dict):
    directory_list = await directory_mapper.select_list(project_id=path['project_id'])
    return {'list': directory_list}


@endpoint({
    'method': 'POST',
    'path': '/app/project/{project_id}/directory',
    'summary': '创建接口分类',
    'requestParam': {
        'path': {
            'project_id!': ['integer', '项目ID'],
        }
    },
    'requestBody': {
        'schema': {
            'name!': 'string',
            'parent!': 'integer',
            'position!': 'integer'
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '接口分类ID']
            }
        }
    }
})
async def insert(directory_mapper: DirectoryMapper, path: dict, body: dict):
    req_data = body['data']
    project_id = path['project_id']
    directory_id = make_unique_id()
    await directory_mapper.insert_directory(
        id=directory_id,
        project_id=project_id,
        name=req_data['name'],
        parent=req_data['parent'],
        position=req_data['position'],
    )
    return {'id': directory_id}


@endpoint({
    'method': 'DELETE',
    'path': '/app/directory/{id}',
    'summary': '删除接口分类',
    'requestParam': {
        'path': {
            'id!': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '接口分类ID']
            }
        }
    }
})
async def delete(directory_mapper: DirectoryMapper, path: dict):
    directory_id = path['id']
    await directory_mapper.delete_by_id(id=directory_id)
    # todo 删除目录下所有接口和mock
    return {'id': directory_id}


@endpoint({
    'method': 'PUT',
    'path': '/app/directory/{id}',
    'summary': '修改接口分类',
    'requestParam': {
        'path': {
            'id!': 'integer',
        }
    },
    'requestBody': {
        'schema': {
            'name!': 'string',
            'parent': 'integer',
            'position': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '接口分类ID']
            }
        }
    }
})
async def update(directory_mapper: DirectoryMapper, path: dict, body: dict):
    req_data = body['data']
    directory_id = path['id']
    await directory_mapper.update_by_id(id=directory_id, **req_data)
    return {'id': directory_id}
