from aiohttp import web
import asyncio
import aiopg
import toml
import lesscli
import pathlib
import os
import wax.controller.directory
import wax.controller.entity
import wax.controller.interface
import wax.controller.mock
import wax.controller.project
import wax.controller.team
import wax.controller.user
from wax.component.pg import init_pg, close_pg, pg_conn_middleware
from wax.component.security import security_middleware
from wax.openapi import show_openapi


@lesscli.add_option('confpath', default='config.toml', help='configure file (.toml format) path, default: config.toml')
def main(confpath):
    """
    start wax backend server
    """
    app = web.Application()
    app['config'] = toml.loads(open(confpath).read())
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    app.middlewares.append(pg_conn_middleware)
    app.middlewares.append(security_middleware)
    app.router.add_route(**wax.controller.user.login)
    app.router.add_route(**wax.controller.user.me_info)
    app.router.add_route(**wax.controller.user.update)
    app.router.add_route(**wax.controller.user.update_password)
    app.router.add_route(**wax.controller.user.create_user)
    app.router.add_route(**wax.controller.team.insert)
    app.router.add_route(**wax.controller.team.update)
    app.router.add_route(**wax.controller.team.delete)
    app.router.add_route(**wax.controller.team.remove_member)
    app.router.add_route(**wax.controller.team.list_member)
    app.router.add_route(**wax.controller.project.create)
    app.router.add_route(**wax.controller.project.query_list)
    app.router.add_route(**wax.controller.project.list_member)
    app.router.add_route(**wax.controller.project.save_member)
    app.router.add_route(**wax.controller.mock.query_list)
    app.router.add_route(**wax.controller.mock.query_detail)
    app.router.add_route(**wax.controller.mock.insert)
    app.router.add_route(**wax.controller.mock.update)
    app.router.add_route(**wax.controller.mock.delete)
    app.router.add_route(**wax.controller.mock.active)
    app.router.add_route(**wax.controller.interface.query_list)
    app.router.add_route(**wax.controller.interface.query_detail)
    app.router.add_route(**wax.controller.interface.insert)
    app.router.add_route(**wax.controller.interface.delete)
    app.router.add_route(**wax.controller.interface.update)
    app.router.add_route(**wax.controller.entity.query_list)
    app.router.add_route(**wax.controller.entity.query_detail)
    app.router.add_route(**wax.controller.entity.insert)
    app.router.add_route(**wax.controller.entity.update)
    app.router.add_route(**wax.controller.entity.delete)
    app.router.add_route(**wax.controller.directory.query_list)
    app.router.add_route(**wax.controller.directory.insert)
    app.router.add_route(**wax.controller.directory.delete)
    app.router.add_route(**wax.controller.directory.update)
    app.router.add_get('/public/openapi.json', show_openapi)
    web.run_app(app, port=app['config']['lessweb']['port'])


@lesscli.add_option('init', type='bool', help='initialize migration')
@lesscli.add_option('upgrade_version', short='-u', long='--up', help='upgrade, head means the latest version')
@lesscli.add_option('downgrade_version', short='-d', long='--down', help='downgrade')
@lesscli.add_option('confpath', default='config.toml', help='configure file (.toml format) path, default: config.toml')
def init_pg_tables(*args, **kwargs):
    """
    init postgres tables
    """
    confpath = kwargs['confpath']
    config = toml.loads(open(confpath).read())
    upgrade_version = kwargs['upgrade_version']
    downgrade_version = kwargs['downgrade_version']
    init_mode = kwargs['init']
    assert bool(upgrade_version) + bool(downgrade_version) + bool(init_mode) == 1, 'wrong arguments. -h for help'

    def parse_version(filename):
        return filename.lower().replace('.sql', '').lstrip('v')

    def version_cmp_key(filename):
        return tuple(map(int, parse_version(filename).split('.')))

    async def go():
        async with aiopg.create_pool(**config['lessweb']['postgres']) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    if init_mode:
                        await cur.execute("""CREATE TABLE wax_schema_history (
  version varchar(40) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (version)
)""")
                    elif upgrade_version:
                        up_path = pathlib.Path('migration/up/')
                        up_path_files = os.listdir('migration/up/')
                        up_path_files.sort(key=version_cmp_key)
                        for filename in up_path_files:
                            version = parse_version(filename)
                            await cur.execute('select version from wax_schema_history where version=%s', (version,))
                            if not await cur.fetchone():
                                sql_content = (up_path / filename).open().read().strip()
                                await cur.execute(sql_content)
                                await cur.execute('insert into wax_schema_history(version) values (%s)', (version,))
                                print(f'upgrade: {version}')
                            if version == parse_version(upgrade_version):
                                break
                    elif downgrade_version:
                        down_path = pathlib.Path('migration/down/')
                        down_path_files = os.listdir('migration/down/')
                        down_path_files.sort(key=version_cmp_key, reverse=True)
                        for filename in down_path_files:
                            version = parse_version(filename)
                            await cur.execute('select version from wax_schema_history where version=%s', (version,))
                            if await cur.fetchone():
                                sql_content = (down_path / filename).open().read().strip()
                                await cur.execute(sql_content)
                                await cur.execute('delete from wax_schema_history where version=%s', (version,))
                                print(f'downgrade: {version}')
                            if version == parse_version(downgrade_version):
                                break
    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())


if __name__ == '__main__':
    cli = lesscli.Application('wax backend')
    cli.add('server', main)
    cli.add('migrate', init_pg_tables)
    cli.run()
