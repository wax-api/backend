from aiohttp import web
import asyncio
import aiopg
import toml
import lesscli
import wax.controller.user
from wax.component.pg import init_pg, close_pg, pg_conn_middleware
from wax.component.security import security_middleware


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
    web.run_app(app, port=app['config']['lessweb']['port'])


@lesscli.add_option('confpath', default='config.toml', help='configure file (.toml format) path, default: config.toml')
def init_pg_tables(confpath):
    """
    init postgres tables
    """
    config = toml.loads(open(confpath).read())

    async def go():
        async with aiopg.create_pool(**config['lessweb']['postgres']) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("""DROP TABLE IF EXISTS tbl_user""")
                    await cur.execute("""
CREATE TABLE tbl_user (
  id bigint NOT NULL,
  avatar varchar(200),
  truename varchar(100) NOT NULL,
  email varchar(200) NOT NULL UNIQUE,
  acl varchar(30) [] NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  read_acl varchar(30) [] NOT NULL,
  write_acl varchar(30) [] NOT NULL,
  PRIMARY KEY (id)
)""")
                    await cur.execute("""
INSERT INTO tbl_user(id, truename, email, acl, read_acl, write_acl)
VALUES(1, '张三', 'null@qq.com', '{"U", "U1"}', '{"U"}', '{"U1"}') 
""")
                    await cur.execute("""DROP TABLE IF EXISTS tbl_auth""")
                    await cur.execute("""
CREATE TABLE tbl_auth (
  user_id bigint NOT NULL,
  password VARCHAR(100) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  read_acl varchar(30) [] NOT NULL,
  write_acl varchar(30) [] NOT NULL,
  PRIMARY KEY (user_id)
)""")
                    await cur.execute("""DROP TABLE IF EXISTS tbl_team""")
                    await cur.execute("""
CREATE TABLE tbl_team (
  id bigint NOT NULL,
  name VARCHAR(200) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  read_acl varchar(30) [] NOT NULL,
  write_acl varchar(30) [] NOT NULL,
  PRIMARY KEY (id)
)""")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())


if __name__ == '__main__':
    cli = lesscli.Application('wax backend')
    cli.add('server', main)
    cli.add('create_table', init_pg_tables)
    cli.run()
