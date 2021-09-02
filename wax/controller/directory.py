from wax.wax_dsl import endpoint


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
async def query():  # todo 查询分类列表
    pass


@endpoint({
    'method': 'POST',
    'path': '/app/directory',
    'description': '创建接口分类',
    'requestBody': {
        'schema': {
            'name!': 'string',
            'parent': 'integer',
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
async def insert():  # todo 创建接口分类
    pass


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
async def delete():  # todo 删除接口分类
    pass


@endpoint({
    'method': 'PUT',
    'path': '/app/directory',
    'description': '修改接口分类',
    'requestBody': {
        'schema': {
            'id!': 'integer',
            'name!': 'string',
            'parent': 'integer',
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
async def update():  # todo 修改接口分类
    pass