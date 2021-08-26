from aiohttp.web import middleware
import aiopg
from aiopg import Pool, Connection, Cursor
import psycopg2.extras
from wax.utils import setdefault


class PgBean:
    refname = 'wax.PgBean'
    conn_refname = f'{refname}.conn'
    cursor_refname = f'{refname}.cursor'
    pool: Pool
    config: dict

    def __init__(self, config):
        self.config = config

    @classmethod
    def from_(cls, app) -> 'PgBean':
        return setdefault(app, cls.refname, lambda: PgBean(app['config']))


async def init_pg(app):
    pg_bean = PgBean.from_(app)
    pg_bean.pool = await aiopg.create_pool(**pg_bean.config['lessweb']['postgres'])


async def close_pg(app):
    pg_bean = PgBean.from_(app)
    pg_bean.pool.close()
    await pg_bean.pool.wait_closed()


@middleware
async def pg_conn_middleware(request, handler):
    async with PgBean.from_(request.app).pool.acquire() as conn:
        request[PgBean.conn_refname] = conn
        async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            request[PgBean.cursor_refname] = cur
            return await handler(request)


def pg_conn(request) -> Connection:
    return request[PgBean.conn_refname]


def pg_cursor(request) -> Cursor:
    return request[PgBean.cursor_refname]
