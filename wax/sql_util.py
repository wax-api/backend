from mako.template import Template
import re
from re import Match
from wax.component.pg import pg_cursor, pg_conn


SELECT_ONE = 1
SELECT_ALL = 2
EXECUTE = 3


class RegexCollect:
    words: list

    def __init__(self):
        self.words = []

    def repl(self, m: Match):
        self.words.append(m.group())
        return '%s'

    def build(self, sql: str, params: dict) -> tuple:
        pattern = r":[\w_]+"
        pg_sql = re.sub(pattern, self.repl, sql)
        pg_params = tuple(params[k[1:]] for k in self.words)
        return pg_sql, pg_params


def _execute(mako_sql, mode):
    async def coro(*args, **kwargs):
        assert len(args) == 1
        cursor = pg_cursor(args[0].request)
        rc = RegexCollect()
        sql = Template(mako_sql).render(**kwargs)
        print(sql)
        pg_sql, pg_params = rc.build(sql, kwargs)
        print(pg_params)
        await cursor.execute(pg_sql, pg_params)
        if mode == SELECT_ONE:
            return await cursor.fetchone()
        elif mode == SELECT_ALL:
            return await cursor.fetchall() or {}
        else:
            return None
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
