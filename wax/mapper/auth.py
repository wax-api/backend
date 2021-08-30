from wax.mapper import Mapper
from wax.sql_util import update, insert


class AuthMapper(Mapper):
    @update('''update tbl_auth set password=:password, updated_at=NOW() 
    where user_id=:user_id
    ''')
    async def update_password(self, *, user_id: int, password: str):
        pass

    @update('''insert tbl_auth(user_id, password)
    values(:user_id, :password)''')
    async def insert(self, *, user_id: int, password: str):
        pass
