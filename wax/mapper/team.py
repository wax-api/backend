from wax.mapper import Mapper
from wax.sql_util import select_one, select_all, update, insert


class TeamMapper(Mapper):
    @select_one('select * from tbl_team T where T.id=:id and T.[READ] limit 1')
    async def select_by_id(self, *, id: int) -> dict:
        pass

    @insert('''insert into tbl_team(id, name, read_acl, write_acl)
    values(:id, :name, :read_acl, :write_acl)''')
    async def insert(self, *, id: int, name: str, read_acl: list, write_acl: list):
        pass
