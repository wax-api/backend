from wax.wax_dsl import endpoint


@endpoint({
    'method': 'GET',
    'path': '/app/entity',
    'description': '查询实体列表',
    'requestParam': {
        'query': {
            'interface_id!': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'list[]': {
                    'id': 'integer',
                    'name': 'string',
                    'interface_id': 'integer',
                }
            }
        }
    }
})
async def query_list():  # todo 查询实体列表
    pass


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
                'name': 'string',
                'interface_id': 'integer',
                'superset_id': ['integer', '超集实体ID'],
                'content': 'string',
            }
        }
    }
})
async def query_detail():  # todo 查询实体详情
    pass


@endpoint({
    'method': 'POST',
    'path': '/app/entity',
    'description': '修改mock',
    'requestBody': {
        'schema': {
            'name!': 'string',
            'interface_id!': 'integer',
            'superset_id': ['integer', '超集实体ID'],
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
async def insert():  # todo 创建实体
    pass


@endpoint({
    'method': 'PUT',
    'path': '/app/entity',
    'description': '修改实体',
    'requestBody': {
        'schema': {
            'id!': 'integer',
            'name': 'string',
            'interface_id': 'integer',
            'superset_id': ['integer', '超集实体ID'],
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
async def update():  # todo 修改实体
    pass


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
async def delete():  # todo 删除实体
    pass
