from wax.mapper import Mapper
from wax.sql_util import select_one, select_all, update, insert, delete


class TeamMapper(Mapper):
    @select_one('select * from tbl_team T where T.id=:id and (T.READ) limit 1')
    async def select_by_id(self, *, id: int) -> dict:
        pass

    @insert('''insert into tbl_team(id, name, read_acl, write_acl)
    select :id, :name, :read_acl, T.write_acl 
    from (select :write_acl as write_acl) T where (T.WRITE)
    ''')
    async def insert_team(self, *, id: int, name: str, read_acl: list, write_acl: list) -> int:
        pass

    @update('''update tbl_team set 
    % if name:
        name=:name
    % endif
    updated_at=NOW() where id=:id and (WRITE)
    ''')
    async def update_by_id(self, *, id: int, name: str=None) -> None:
        pass

    @delete('''delete from tbl_team where id=:id and (WRITE)''')
    async def delete_by_id(self, *, id: int) -> None:
        pass

    @insert('''insert into tbl_team_user(id, team_id, user_id)
    select :id, T.id, :user_id AS uid from tbl_team T
    where T.id=:team_id and (T.WRITE) limit 1
    ''')
    async def add_team_member(self, *, id: int, team_id: int, user_id: int) -> None:
        pass

    @delete('''delete from tbl_team_user TU
     using tbl_team T
     where T.id=TU.team_id and T.id=:team_id and (T.WRITE) 
    ''')
    async def remove_team_member(self, *, team_id: int) -> None:
        pass
