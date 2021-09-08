from wax.wax_dsl import endpoint
from wax.component.security import AuthUser
from wax.mapper.directory import DirectoryMapper
from wax.utils import make_unique_id


@endpoint({
    'method': 'GET',
    'path': '/app/directory',
    'description': '查询分类列表',
    'requestParam': {
        'query': {
            'project_id!': 'integer',
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
async def query_list(directory_mapper: DirectoryMapper, query: dict):
    directory_list = await directory_mapper.select_list(project_id=query['project_id'])
    return {'list': directory_list}


@endpoint({
    'method': 'POST',
    'path': '/app/directory',
    'description': '创建接口分类',
    'requestBody': {
        'schema': {
            'project_id!': 'integer',
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
async def insert(directory_mapper: DirectoryMapper, auth_user: AuthUser, body: dict):
    req_data = body['data']
    project_id = req_data['project_id']
    assert f'P{project_id}' in auth_user.acl, '无创建接口分类权限'
    directory_id = make_unique_id()
    await directory_mapper.insert_directory(
        id=directory_id,
        project_id=project_id,
        name=req_data['name'],
        parent=req_data['parent'],
        position=req_data['position'],
        write_acl=[f'P{project_id}']
    )
    return {'id': directory_id}


@endpoint({
    'method': 'DELETE',
    'path': '/app/directory/{id}',
    'description': '删除接口分类',
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
    assert await directory_mapper.writable(id=directory_id), '无删除接口分类权限'
    await directory_mapper.delete_by_id(id=directory_id)
    # todo 删除目录下所有接口
    return {'id': directory_id}


@endpoint({
    'method': 'PUT',
    'path': '/app/directory',
    'description': '修改接口分类',
    'requestBody': {
        'schema': {
            'id!': 'integer',
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
async def update(directory_mapper: DirectoryMapper, body: dict):
    req_data = body['data']
    directory_id = req_data['id']
    assert await directory_mapper.writable(id=directory_id), '无修改接口分类权限'
    await directory_mapper.update_by_id(**req_data)
    return {'id': directory_id}
