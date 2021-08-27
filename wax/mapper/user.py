from wax.mapper import Mapper
from wax.sql_util import select_one, update


class UserMapper(Mapper):
    @select_one('select * from tbl_user where id=:id limit 1')
    async def select_by_id(self, *, id: int) -> dict:
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
