from wax.mapper import Mapper
from wax.sql_util import update, insert, select_one, select_all, delete


class MockMapper(Mapper):
    @select_one('''select id, project_id, interface_iid, status_code, content_type, 
    mockjs, content, type, headers, active,
    created_at, updated_at, create_user_id, update_user_id 
    from tbl_mock where id=:id''')
    async def select_by_id(self, *, id: int):
        pass

    @select_one('''select * from tbl_mock where
    project_id=:project_id and interface_iid=:interface_iid and active=1
    ''')
    async def select_by_active(self, *, project_id: int, interface_iid: int):
        pass

    @select_all('''select id, name, status_code, content_type, active from tbl_mock 
    where project_id=:project_id and interface_iid=:interface_iid
    % if status_code:
        and status_code=:status_code,
    % endif 
    order by id desc
    ''')
    async def select_list(self, *, project_id: int, interface_iid: int, status_code: str=None):
        pass

    @update('''update tbl_mock set
    % if status_code is not None:
        status_code=:status_code, 
    % endif
    % if content_type is not None:
        content_type=:content_type, 
    % endif
    % if mockjs is not None:
        mockjs=:mockjs, 
    % endif
    % if content is not None:
        content=:content, 
    % endif
    % if type is not None:
        type=:type, 
    % endif
    % if headers is not None:
        headers=:headers, 
    % endif
    % if active is not None:
        active=:active, 
    % endif
    updated_at=NOW() where id=:id
    ''')
    async def update_by_id(self, *, id: int, status_code: str=None, content_type: str=None, mockjs: str=None, content: str=None, type: str=None, headers: str=None, active: int=None):
        pass

    @update('''update tbl_mock set active=0 where project_id=:project_id and interface_iid=:interface_iid''')
    async def unactive_all(self, *, project_id: int, interface_iid: int):
        pass

    @insert('''insert tbl_mock(id, project_id, interface_iid, status_code, content_type, mockjs, content, type, headers, active)
    values (:id, :project_id, :interface_iid, :status_code, :content_type, :mockjs, :content, :type, :headers, :active)
    ''')
    async def insert_mock(self, *, id: int, project_id: int, interface_iid: int, status_code: str, content_type: str, mockjs: str, content: str, type: str, headers: str, active: int):
        pass

    @delete('''delete from tbl_mock where id=:id''')
    async def delete_by_id(self, *, id: int):
        pass
