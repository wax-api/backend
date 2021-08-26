from typing import Optional

from wax.mapper import Mapper
from wax.sql_util import select_one


class UserMapper(Mapper):
    @select_one('select * from tbl_user where id=:id limit 1')
    async def select_by_id(self, *, id: int) -> Optional[dict]:
        pass