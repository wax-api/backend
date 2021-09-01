from aiohttp import web
import asyncio
import aiopg
import toml
import lesscli
import wax.controller.user
import wax.controller.team
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
    app.router.add_route(**wax.controller.user.update_password)
    app.router.add_route(**wax.controller.team.insert)
    app.router.add_route(**wax.controller.team.update)
    app.router.add_route(**wax.controller.team.delete)
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
  team_id bigint NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  read_acl text [] NOT NULL,
  write_acl text [] NOT NULL,
  PRIMARY KEY (id)
)""")
                    await cur.execute("""
INSERT INTO tbl_user(id, truename, email, team_id, read_acl, write_acl)
VALUES(1, '张三', 'null@qq.com', 0, '{"U"}', '{"U1"}') 
""")
                    await cur.execute("""DROP TABLE IF EXISTS tbl_auth""")
                    await cur.execute("""
CREATE TABLE tbl_auth (
  user_id bigint NOT NULL,
  password VARCHAR(100) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  read_acl text [] NOT NULL,
  write_acl text [] NOT NULL,
  PRIMARY KEY (user_id)
)""")
                    await cur.execute("""
INSERT INTO tbl_auth(user_id, password, read_acl, write_acl)
VALUES(1, '$2b$12$29jP3EvsgzaF22k906PdDeflgum5ZalaolH4fbe8aeLxrl1KuwIkG', '{"U1"}', '{"U1"}')
""")  # password=12345678
                    await cur.execute("""DROP TABLE IF EXISTS tbl_acl""")
                    await cur.execute("""
CREATE TABLE tbl_acl (
  user_id bigint NOT NULL,
  acl text [] NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  read_acl text [] NOT NULL,
  write_acl text [] NOT NULL,
  PRIMARY KEY (user_id)
)""")
                    await cur.execute("""
INSERT INTO tbl_acl(user_id, acl, read_acl, write_acl)
VALUES(1, '{"U", "U1"}', '{"U1"}', '{"U"}')
""")
                    await cur.execute("""DROP TABLE IF EXISTS tbl_team""")
                    await cur.execute("""
CREATE TABLE tbl_team (
  id bigint NOT NULL,
  name VARCHAR(200) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  read_acl text [] NOT NULL,
  write_acl text [] NOT NULL,
  PRIMARY KEY (id)
)""")
                    await cur.execute("""DROP TABLE IF EXISTS tbl_team_user""")
                    await cur.execute("""
                    CREATE TABLE tbl_team_user (
  id bigint NOT NULL,
  team_id bigint NOT NULL,
  user_id bigint NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (id)
)""")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())


if __name__ == '__main__':
    cli = lesscli.Application('wax backend')
    cli.add('server', main)
    cli.add('create_table', init_pg_tables)
    cli.run()
