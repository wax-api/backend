from wax.mapper import Mapper
from wax.sql_util import select_one, select_range, update, insert, delete


class ProjectMapper(Mapper):
    @select_one('select * from tbl_project P where P.id=:id limit 1')
    async def select_by_id(self, *, id: int) -> dict:
        pass

    @insert('''insert into tbl_project(id, team_id, name, remark, visibility)
    values(:id, :team_id, :name, :remark, :visibility) 
    ''')
    async def insert_project(self, *, id: int, team_id: int, name: str, remark: str, visibility: str) -> int:
        pass

    @update('''update tbl_project set 
    % if name:
        name=:name,
    % endif
    % if remark:
        remark=:remark,
    % endif
    % if visibility:
        visibility=:visibility,
    % endif
    updated_at=NOW() where id=:id
    ''')
    async def update_by_id(self, *, id: int, name: str=None, remark: str=None, visibility: str=None) -> None:
        pass

    @delete('''delete from tbl_project where id=:id''')
    async def delete_by_id(self, *, id: int) -> int:
        pass

    @select_range('''select id, name, remark, visibility
    from tbl_project
    where team_id=:team_id
    order by id desc limit :limit offset :offset 
    ''')
    async def query_list(self, *, limit: int, offset: int, team_id: int) -> dict:
        pass

    @insert('''insert into tbl_project_user(id, project_id, user_id, role)
    values(:id, :project_id, :user_id, :role)
    ''')
    async def add_project_member(self, *, id: int, project_id: int, user_id: int, role: str) -> int:
        pass

    @update('''update tbl_project_user PU set
    PU.role=:role, PU.updated_at=NOW()
    where PU.project_id=:project_id and PU.user_id=:user_id
    ''')
    async def update_project_member(self, *, project_id: int, user_id: int, role: str) -> int:
        pass

    @select_one('''select PU.role from tbl_project_user PU
    where PU.project_id=:project_id and PU.user_id=:user_id limit 1
    ''')
    async def select_project_role(self, *, project_id: int, user_id: int) -> dict:
        pass

    @delete('''delete from tbl_project_user PU
    where PU.project_id=:project_id
    % if user_id:
        and PU.user_id=:user_id
    % endif
    ''')
    async def remove_project_member(self, *, project_id: int, user_id: int=None) -> int:
        pass

    @select_range('''select U.id, U.avatar, U.truename, U.email, U.team_id, U.created_at, U.updated_at,
    PU.role AS project_role
    from tbl_project_user PU
    left join tbl_user U on U.id=PU.user_id
    left join tbl_project P on P.id=PU.project_id
    where P.id=:project_id
    order by U.id desc limit :limit offset :offset
    ''')
    async def query_member_list(self, *, limit: int, offset: int, project_id: int) -> dict:
        pass