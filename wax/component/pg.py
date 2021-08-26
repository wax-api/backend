from aiohttp.web import middleware
import aiopg
import psycopg2.extras


async def init_pg(app):
    config = app['config']
    app['pg'] = await aiopg.create_pool(**config['lessweb']['postgres'])


async def close_pg(app):
    app['pg'].close()
    await app['pg'].wait_closed()


@middleware
async def pg_conn_middleware(request, handler):
    async with request.app['pg'].acquire() as conn:
        request['pg_conn'] = conn
        async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            request['pg_cur'] = cur
            return await handler(request)
