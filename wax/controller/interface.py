from wax.wax_dsl import endpoint


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
async def query_list():  # todo 查询接口列表
    pass


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
                'created_by': {
                    'user_id': 'integer',
                    'truename': 'string',
                },
                'updated_at': 'string',
                'updated_by': {
                    'user_id': 'integer',
                    'truename': 'string',
                },
                'endpoint': 'string',
            }
        }
    }
})
async def query_detail():  # todo 查询接口详情
    pass


@endpoint({
    'method': 'POST',
    'path': '/app/interface',
    'description': '创建接口',
    'requestBody': {
        'schema': {
            'name!': 'string',
            'parent': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'name': 'string',
                'method': 'string',
                'path': 'string',
                'directory_id': 'integer',
            }
        }
    }
})
async def insert():  # todo 创建接口
    pass


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
async def delete():  # todo 删除接口
    pass


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
async def update():  # todo 修改接口
    pass