from wax.mapper import Mapper
from wax.sql_util import select_one, update, insert


class UserMapper(Mapper):

    @select_one('''select id from tbl_user U where U.id=:id and (U.WRITE) limit 1''')
    async def writable(self, *, id: int) -> dict:
        pass

    @select_one('''select id,avatar,truename,email,team_id,created_at,updated_at 
    from tbl_user U where U.id=:id and (U.READ) limit 1
    ''')
    async def select_by_id(self, *, id: int) -> dict:
        pass

    @select_one('select * from tbl_user U where U.email=:email and (U.READ) limit 1')
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
    updated_at=NOW() where id=:id
    ''')
    async def update_by_id(self, *, id: int, avatar: str=None, truename: str=None, email: str=None) -> None:
        pass

    @insert('''insert into tbl_user(id, truename, email, team_id, read_acl, write_acl)
    values(:id, :truename, :email, :team_id, :read_acl, :write_acl)
    ''')
    async def insert_user(self, *, id: int, truename: str, email: str, team_id: int, read_acl: list, write_acl: list) -> int:
        pass

