from aiohttp.web import Request, Response, json_response
from wax.jwt_util import JWTUtil
from wax.utils import timestamp
import psycopg2.extras


def wax_endpoint(endpoint):
    def f(g):
        return g
    return f


@wax_endpoint({
    'method': 'POST',
    'path': '/login',
    'requestBody': {
        'schema': {
            'email!': 'string',
            'password!': 'string'
        }
    },
    'response': {
        '200': {
            'schema': {
                'token': 'string'
            }
        }
    }
})
async def login(request: Request) -> Response:
    req_data = await request.json()
    print(req_data)
    async with request.app['pg_conn'].cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        await cur.execute('select * from tbl_user limit 1')
        user_db = await cur.fetchone()
        print(user_db)
        token = JWTUtil(None).encrypt(user_db['id'], 'USER', timestamp(86400))
        return json_response({'token': token})
