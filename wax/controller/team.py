from aiohttp.web import Request


from wax.component.security import auth_user
from wax.mapper.team import TeamMapper
from wax.wax_dsl import endpoint, Keys, input_body
from wax.utils import make_unique_id


@endpoint({
    'method': 'POST',
    'path': '/app/team',
    'description': '创建团队',
    'requestBody': {
        'schema': {
            'name!': ['string', '团队名称', {'minLength': 2}],
        }
    },
    'response': {
        '200': {
            'id': ['integer', '团队ID']
        }
    }
})
async def insert(request: Request):
    team_mapper = TeamMapper(request)
    user_id = auth_user(request).user_id
    req_data = input_body(request)
    team_id = make_unique_id()
    await team_mapper.insert(
        id=team_id, name=req_data['name'],
        read_acl=[f'U{user_id}'],
        write_acl=[f'U{user_id}'],
    )
    return {'id': team_id}
