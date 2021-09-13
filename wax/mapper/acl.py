from wax.mapper import Mapper
from wax.sql_util import update, select_one, insert, delete


class ACLMapper(Mapper):
    """
    ACL的定义：
        G => 游客
        U/{user_id} => 指定的用户
        TA/{team_id} => 团队管理员
        T/{team_id} => 团队成员
        PA/{project_id} => 项目管理员
        P/{project_id} => 项目成员
    """
    @select_one('''select user_id, acl from tbl_acl where user_id=:user_id''')
    async def select_by_user_id(self, *, user_id: int):
        pass

    @update('update tbl_acl set acl=(acl||:adding_acls), updated_at=NOW() where (acl&&:acls)')
    async def add_acls(self, *, acls: list, adding_acls: list) -> None:
        pass

    @update('update tbl_acl set acl=(acl||:adding_acls), updated_at=NOW() where user_id=:user_id')
    async def add_acls_by_user_id(self, *, user_id: int, adding_acls: list) -> None:
        pass

    @update('''update tbl_acl set acl=array_remove(acl, :removing_acl), updated_at=NOW() where (acl&&:acls)''')
    async def remove_acl(self, *, acls: list, removing_acl: str) -> None:
        pass

    @update('''update tbl_acl set acl=array_remove(acl, :removing_acl), updated_at=NOW() where user_id=:user_id''')
    async def remove_acl_by_user_id(self, *, user_id: int, removing_acl: str) -> None:
        pass

    @insert('''insert into tbl_acl(user_id, acl)
    values(:user_id, :acl)
    ''')
    async def insert_acl(self, *, user_id: int, acl: list):
        pass

    @delete('''delete from tbl_acl where user_id=:user_id''')
    async def delete_by_user_id(self, *, user_id: int):
        pass
