from aiohttp.web import middleware
import aiopg


async def init_pg(app):
    config = app['config']
    app['pg'] = await aiopg.create_pool(**config['lessweb']['postgres'])


async def close_pg(app):
    app['pg'].close()
    await app['pg'].wait_closed()


@middleware
async def conn_middleware(request, handler):
    request['pg'] = await request.app['pg']._acquire()
    try:
        return await handler(request)
    finally:
        await request.app['pg'].release(request['pg'])
