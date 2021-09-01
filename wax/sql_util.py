from mako.template import Template
import re
from re import Match
from wax.component.pg import pg_cursor
from wax.component.security import AuthUser
from wax.inject_util import get_request_ctx


SELECT_ONE = 1
SELECT_ALL = 2
EXECUTE = 3


class RegexCollect:
    words: list

    def __init__(self):
        self.words = []

    def repl(self, m: Match):
        word = m.group()
        self.words.append(word[2:])
        return word[0] + '%s'

    def build(self, sql: str, params: dict) -> tuple:
        sql = sql.replace('READ)', 'read_acl && :acl)')
        sql = sql.replace('WRITE)', 'write_acl && :acl)')
        pattern = r"[^:]:[\w_]+"
        pg_sql = re.sub(pattern, self.repl, sql)
        pg_params = tuple(params[k] for k in self.words)
        return pg_sql, pg_params


def _execute(mako_sql, mode):
    async def coro(*args, **kwargs):
        assert len(args) == 1, 'self requires a mapper instance'
        request = args[0].request
        cursor = pg_cursor(request)
        acl = get_request_ctx(request, AuthUser, 'auth_user').acl
        rc = RegexCollect()
        sql = Template(mako_sql).render(**kwargs).strip()
        print(sql)
        if mode == SELECT_ONE or mode == SELECT_ALL:
            if 'READ)' not in sql:
                raise TypeError('missing (READ) in sql')
        else:
            if 'WRITE)' not in sql:
                raise TypeError('missing (WRITE) in sql')
        pg_sql, pg_params = rc.build(sql, {**kwargs, 'acl': acl})
        print(pg_sql, '=>', pg_params)
        await cursor.execute(pg_sql, pg_params)
        if mode == SELECT_ONE:
            return await cursor.fetchone() or {}
        elif mode == SELECT_ALL:
            return await cursor.fetchall()
        else:
            return cursor.rowcount
    return lambda method: coro or 1


def select_one(sql):
    return _execute(sql, SELECT_ONE)


def select_all(sql):
    return _execute(sql, SELECT_ALL)


def insert(sql):
    return _execute(sql, EXECUTE)


def update(sql):
    return _execute(sql, EXECUTE)


def delete(sql):
    return _execute(sql, EXECUTE)
