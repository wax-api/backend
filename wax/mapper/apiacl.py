from wax.mapper import Mapper
from wax.sql_util import update, select_one, insert


class APIACLMapper(Mapper):
    """
    ACL的定义：
        * => 允许匿名访问
        U/* => 任何用户
        U/{user_id} => 指定的用户
        TA/{team_id} => 团队管理员
        T/{team_id} => 团队成员
        PA/{project_id} => 项目管理员
        P/{project_id} => 项目成员
    """
    @select_one('''select * from tbl_api_acl where method=:method and path=:path''')
    async def select_unique(self, *, method: str, path: str):
        pass

    @update('update tbl_api_acl set acl=(acl||:adding_acls), updated_at=NOW() where (acl&&:acls)')
    async def add_acls(self, *, acls: list, adding_acls: list) -> None:
        pass

    @update('update tbl_api_acl set acl=(acl||:adding_acls), updated_at=NOW() where method=:method and path=:path')
    async def add_acls_unique(self, *, method: str, path: str, adding_acls: list) -> None:
        pass

    @update('''update tbl_api_acl set acl=array_remove(acl, :removing_acl), updated_at=NOW() where (acl&&:acls)''')
    async def remove_acl(self, *, acls: list, removing_acl: str) -> None:
        pass

    @update('''update tbl_api_acl set acl=array_remove(acl, :removing_acl), updated_at=NOW() where method=:method and path=:path''')
    async def remove_acl_unique(self, *, method: str, path: str, removing_acl: str) -> None:
        pass

    @insert('''insert into tbl_api_acl(id, method, path, acl)
    values(:id, :method, :path, :acl)
    ''')
    async def insert_acl(self, *, id: int, method: str, path: str, acl: list):
        pass
