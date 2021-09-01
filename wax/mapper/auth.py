from wax.mapper import Mapper
from wax.sql_util import update, insert, select_one


class AuthMapper(Mapper):
    @select_one('''select user_id, password from tbl_auth where user_id=:user_id and (READ)''')
    async def select_by_user_id(self, *, user_id: int):
        pass

    @update('''update tbl_auth set password=:password, updated_at=NOW() 
    where user_id=:user_id and (WRITE)
    ''')
    async def update_password(self, *, user_id: int, password: str):
        pass

    @insert('''insert tbl_auth(user_id, password)
    values(:user_id, :password, :read_acl, :write_acl)''')
    async def insert_auth(self, *, user_id: int, password: str, read_acl: list, write_acl: list):
        pass
