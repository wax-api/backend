from wax.mapper import Mapper
from wax.sql_util import select_one, select_range, update, insert, delete


class TeamMapper(Mapper):
    @select_one('select id from tbl_team T where T.id=:id limit 1')
    async def writable(self, *, id: int) -> dict:
        pass

    @select_one('select * from tbl_team T where T.id=:id limit 1')
    async def select_by_id(self, *, id: int) -> dict:
        pass

    @insert('''insert into tbl_team(id, name, read_acl, write_acl)
    values(:id, :name, :read_acl, :write_acl) 
    ''')
    async def insert_team(self, *, id: int, name: str, read_acl: list, write_acl: list) -> int:
        pass

    @update('''update tbl_team set 
    % if name:
        name=:name,
    % endif
    updated_at=NOW() where id=:id
    ''')
    async def update_by_id(self, *, id: int, name: str=None) -> None:
        pass

    @delete('''delete from tbl_team where id=:id''')
    async def delete_by_id(self, *, id: int) -> None:
        pass

    @insert('''insert into tbl_team_user(id, team_id, user_id)
    values(:id, :team_id, :user_id)
    ''')
    async def add_team_member(self, *, id: int, team_id: int, user_id: int) -> int:
        pass

    @delete('''delete from tbl_team_user TU
     where TU.team_id=:team_id
     % if user_id:
        and TU.user_id=:user_id
     % endif 
    ''')
    async def remove_team_member(self, *, team_id: int, user_id: int) -> None:
        pass

    @select_range('''select U.id, U.avatar, U.truename, U.email, U.created_at, U.updated_at
    ,TU.role AS team_role
    % if project_id:
        ,PU.role AS project_role
    % else
        ,null AS project_role
    % endif
    from tbl_team_user TU 
    left join tbl_user U on TU.user_id=U.id
    left join tbl_team T on T.id=:team_id
    % if project_id:
        left join tbl_project_user PU on PU.user_id=TU.user_id and PU.project_id=:project_id
        left join tbl_project P on P.id=PU.project_id
    % endif
    where TU.team_id=:team_id
    % if keyword:
        and (U.truename LIKE :keyword or U.email LIKE :keyword)
    % endif
    order by Tu.id desc limit :limit offset :offset
    ''')
    async def select_team_member(self, *, offset: int, limit: int, team_id: int, keyword: str, project_id: int) -> list:
        pass
