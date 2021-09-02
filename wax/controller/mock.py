from wax.wax_dsl import endpoint


@endpoint({
    'method': 'GET',
    'path': '/app/mock',
    'description': '查询mock列表',
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
async def query_list():  # todo 查询mock列表
    pass


@endpoint({
    'method': 'GET',
    'path': '/app/mock/{id}',
    'description': '创建mock',
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
async def query_detail():  # todo 查询mock详情
    pass


@endpoint({
    'method': 'POST',
    'path': '/app/mock',
    'description': '创建mock',
    'requestBody': {
        'schema': {
            'name!': 'string',
            'interface_id!': 'integer',
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
async def insert():  # todo 创建mock
    pass


@endpoint({
    'method': 'PUT',
    'path': '/app/mock',
    'description': '修改mock',
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
            'active': 'integer',
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
async def update():  # todo 修改mock
    pass


@endpoint({
    'method': 'DELETE',
    'path': '/app/mock/{id}',
    'description': '删除接口',
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
async def delete():  # todo 删除mock
    pass
