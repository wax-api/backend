from wax.mapper import Mapper
from wax.sql_util import update, insert, select_one, select_all, delete


class InterfaceMapper(Mapper):
    @select_one('''select id from tbl_interface where project_id=:project_id and iid=:iid limit 1''')
    async def select_by_iid(self, *, project_id: int, iid: int):
        pass

    @select_one('''select id, name, method, path, directory_iid, status, endpoint, 
    created_at, updated_at, create_user_id, update_user_id 
    from tbl_interface where id=:id''')
    async def select_by_id(self, *, id: int):
        pass

    @select_all('''select id, name, method, path, directory_iid from tbl_interface 
    where project_id=:project_id
    % if directory_iid:
        and directory_iid=:directory_iid,
    % endif 
    order by id desc
    ''')
    async def select_list(self, *, project_id: int, directory_iid: int=None):
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
    % if directory_iid is not None:
        directory_iid=:directory_iid,
    % endif
    % if status is not None:
        status=:status,
    % endif
    % if endpoint is not None:
        endpoint=:endpoint,
    % endif
    updated_at=NOW() where id=:id
    ''')
    async def update_by_id(self, *, id: int, name: str=None, method: str=None, path: str=None, directory_iid: int=None, status: str=None, endpoint: str=None):
        pass

    @insert('''insert tbl_interface(id, iid, project_id, directory_iid, directory_iid, name, method, path)
    values (:id, :iid, :project_id, :directory_iid, :name, :method, :path)
    ''')
    async def insert_interface(self, *, id: int, iid: int, project_id: int, directory_iid: int, name: str, method: str, path: str):
        pass

    @delete('''delete from tbl_interface where id=:id''')
    async def delete_by_id(self, *, id: int):
        pass
