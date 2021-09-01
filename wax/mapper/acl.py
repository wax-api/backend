from wax.mapper import Mapper
from wax.sql_util import update, select_one


class ACLMapper(Mapper):
    """
    ACL的定义：
        U => 任何用户
        U{user_id} => 指定的用户
        TA{team_id} => 团队管理员
        T{team_id} => 团队成员
        PA{project_id} => 项目管理员
        P{project_id} => 项目成员
    """
    @select_one('''select user_id, acl from tbl_acl where user_id=:user_id and (READ)''')
    async def select_by_user_id(self, *, user_id: int):
        pass

    @update('update tbl_acl set acl=(acl||:acls), updated_at=NOW() where user_id=:user_id and (WRITE)')
    async def add_acls(self, *, user_id: int, acls: list) -> None:
        pass

    @update('update tbl_acl set acl=array_remove(acl, :removing_acl), updated_at=NOW() where user_id=:user_id and (WRITE)')
    async def remove_acl(self, *, user_id: int, removing_acl: str) -> None:
        pass
