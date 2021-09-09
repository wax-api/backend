from wax.mapper import Mapper
from wax.sql_util import update, insert, select_one, select_all, delete


class InterfaceMapper(Mapper):
    @select_one('''select id from tbl_interface where id=:id and (WRITE)''')
    async def writable(self, *, id: int):
        pass

    @select_one('''select id, name, method, path, directory_id, status, endpoint, 
    created_at, updated_at, create_user_id, update_user_id 
    from tbl_interface where id=:id and (READ)''')
    async def select_by_id(self, *, id: int):
        pass

    @select_all('''select id, name, method, path, directory_id from tbl_interface 
    where project_id=:project_id
    % if directory_id:
        and directory_id=:directory_id,
    % endif 
    and (READ) order by id desc
    ''')
    async def select_list(self, *, project_id: int, directory_id: int=None):
        pass

    @update('''update tbl_interface set
    % if name:
        name=:name,
    % endif
    % if method is not None:
        method=:method,
    % endif
    % if path is not None:
        path=:path,
    % endif
    % if directory_id is not None:
        directory_id=:directory_id,
    % endif
    % if status is not None:
        status=:status,
    % endif
    % if endpoint is not None:
        endpoint=:endpoint,
    % endif
    updated_at=NOW() where id=:id
    ''')
    async def update_by_id(self, *, id: int, name: str=None, method: str=None, path: str=None, directory_id: int=None, status: str=None, endpoint: str=None):
        pass

    @insert('''insert tbl_interface(id, project_id, directory_id, name, method, path, read_acl, write_acl)
    select :id, :project_id, :directory_id, :name, :method, :path, T.read_acl, :write_acl
    from (select id, read_acl from tbl_project where id=:project_id) T''')
    async def insert_interface(self, *, id: int, project_id: int, directory_id: int, name: str, method: str, path: str, write_acl: list):
        pass

    @delete('''delete from tbl_interface where id=:id''')
    async def delete_by_id(self, *, id: int):
        pass