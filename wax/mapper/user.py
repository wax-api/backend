from wax.mapper import Mapper
from wax.sql_util import select_one, update


class UserMapper(Mapper):
    """
    ACL的定义：
        U => 任何用户
        U{user_id} => 指定的用户
        TA{team_id} => 团队管理员
        T{team_id} => 团队成员
        PA{project_id} => 项目管理员
        P{project_id} => 项目成员
    """
    @select_one('select * from tbl_user U where U.id=:id and U.[READ] limit 1')
    async def select_by_id(self, *, id: int) -> dict:
        pass

    @select_one('select * from tbl_user U where U.email=:email and U.[READ] limit 1')
    async def select_by_email(self, *, email: str) -> dict:
        pass

    @update('''update tbl_user set
    % if avatar:
        avatar=:avatar,
    % endif
    % if truename:
        truename=:truename,
    % endif
    % if email:
        email=:email,
    % endif
    updated_at=NOW() where id=:id and [WRITE]
    ''')
    async def update_by_id(self, *, id: int, avatar: str=None, truename: str=None, email: str=None) -> None:
        pass

    @update('update tbl_user set acl=acl||:acls, updated_at=NOW() where id=:id')
    async def add_acls(self, *, id: int, acls: list) -> None:
        pass

    @update('update tbl_user set acl=array_remove(acl, :removing_acl), updated_at=NOW() where id=:id')
    async def remove_acl(self, *, id: int, removing_acl: str) -> None:
        pass
