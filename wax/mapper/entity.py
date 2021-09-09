from wax.mapper import Mapper
from wax.sql_util import update, insert, select_one, select_all, delete


class EntityMapper(Mapper):
    @select_one('''select id from tbl_entity where id=:id and (WRITE)''')
    async def writable(self, *, id: int):
        pass

    @select_one('''select id, name, content, 
    created_at, updated_at, create_user_id, update_user_id 
    from tbl_entity where id=:id and (READ)''')
    async def select_by_id(self, *, id: int):
        pass

    @select_all('''select id, name, superset_id from tbl_entity 
    where project_id=:project_id
    % if superset_id:
        and superset_id=:superset_id,
    % endif 
    and (READ) order by id desc
    ''')
    async def select_list(self, *, project_id: int, superset_id: int=None):
        pass

    @update('''update tbl_entity set
    % if name:
        name=:name,
    % endif
    % if content is not None:
        content=:content,
    % endif
    updated_at=NOW() where id=:id
    ''')
    async def update_by_id(self, *, id: int, name: str=None, content: str=None):
        pass

    @insert('''insert tbl_entity(id, project_id, superset_id, name, content, read_acl, write_acl)
    select :id, :project_id, :superset_id, :name, :content, T.read_acl, :write_acl
    from (select id, read_acl from tbl_project where id=:project_id) T''')
    async def insert_entity(self, *, id: int, project_id: int, superset_id: int, name: str, content: str, write_acl: list):
        pass

    @delete('''delete from tbl_entity where id=:id''')
    async def delete_by_id(self, *, id: int):
        pass
