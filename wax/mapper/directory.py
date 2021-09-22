from wax.mapper import Mapper
from wax.sql_util import update, insert, select_one, select_all, delete


class DirectoryMapper(Mapper):
    @select_one('''select id, name, parent from tbl_directory where id=:id''')
    async def select_by_id(self, *, id: int):
        pass

    @select_all('''select id, name, parent from tbl_directory 
    where project_id=:project_id order by position
    ''')
    async def select_list(self, *, project_id: int):
        pass

    @update('''update tbl_directory set
    % if name:
        name=:name,
    % endif
    % if parent is not None:
        parent=:parent,
    % endif
    % if position is not None:
        position=:position,
    % endif
    updated_at=NOW() where id=:id
    ''')
    async def update_by_id(self, *, id: int, name: str, parent: int=None, position: int=None):
        pass

    @insert('''insert tbl_directory(id, project_id, name, parent, position)
    values (:id, :project_id, :name, :parent, :position)''')
    async def insert_directory(self, *, id: int, project_id: int, name: str, parent: int, position: int):
        pass

    @delete('''delete from tbl_directory where id=:id''')
    async def delete_by_id(self, *, id: int):
        pass
