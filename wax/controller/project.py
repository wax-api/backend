from wax.wax_dsl import endpoint


@endpoint({
    'method': 'POST',
    'path': '/app/project',
    'description': '创建项目',
    'requestBody': {
        'schema': {
            'name': ['string', '项目名称'],
            'remark': ['string', '项目描述'],
            'visibility': ['string', '可见度', {'enum': ['public', 'private']}]
        }
    },
    'response': {
        '200': {
            'schema': {
                'id': ['integer', '项目ID']
            }
        }
    }
})
async def create_project():  # todo 创建项目
    pass


@endpoint({
    'method': 'GET',
    'path': '/app/project',
    'description': '查询项目列表',
    'requestParam': {
        'query': {
            'offset': 'integer',
            'limit': 'integer',
        }
    },
    'response': {
        '200': {
            'schema': {
                'total': 'integer',
                'offset': 'integer',
                'limit': 'integer',
                'list[]': {
                    'id': ['integer', '项目ID'],
                    'name': ['string', '项目名称'],
                    'remark': ['string', '项目描述'],
                    'visibility': ['string', '可见度', {'enum': ['public', 'private']}]
                }
            }
        }
    }
})
async def list_project():  # todo 查询项目列表
    pass


@endpoint({
    'method': 'GET',
    'path': '/app/project/{id}/member',
    'description': '查询团队成员列表',
    'requestParam': {
        'query': {
            'id!': ['integer', '团队ID'],
            'offset': 'integer',
            'limit': 'integer',
        }
    },
    'response': {
        '200': {
                'total': 'integer',
                'offset': 'integer',
                'limit': 'integer',
                'list[]': {
                    'id': ['integer', '用户ID'],
                    'avatar?': 'string',
                    'truename': 'string',
                    'email': 'string',
                    'team_id': 'integer',
                    'created_at': 'string',
                    'updated_at': 'string',
                    'project_role?': ['string', {'enum': ['admin', 'member']}]
                }
            }
    }
})
async def list_member():  # todo 查询团队成员列表
    pass


@endpoint({
    'method': 'PUT',
    'path': '/app/project/member',
    'description': '添加或编辑项目成员',
    'requestBody': {
        'schema': {
            'user_id!': ['integer', '用户ID'],
            'role!': ['string', '成员角色', {'enum': ['admin', 'member']}],
        }
    }
})
async def edit_member():  # todo 添加或编辑项目成员
    pass
