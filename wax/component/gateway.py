from wax.mapper.acl import ACLMapper
from wax.mapper.apiacl import APIACLMapper
from wax.utils import make_unique_id


class Gateway:
    aclmapper: ACLMapper
    apiaclmapper: APIACLMapper

    def __init__(self, aclmapper: ACLMapper, apiaclmapper: APIACLMapper):
        self.aclmapper = aclmapper
        self.apiaclmapper = apiaclmapper

    async def put_user_acl(self, user_id: int, pop_acls: list=None, add_acls: list=None):
        if not await self.aclmapper.select_by_user_id(user_id=user_id):
            await self.aclmapper.insert_acl(user_id=user_id, acl=[])
        for acl in pop_acls or []:
            await self.aclmapper.remove_acl_by_user_id(user_id=user_id, removing_acl=acl)
        if add_acls:
            await self.aclmapper.add_acls_by_user_id(user_id=user_id, adding_acls=add_acls)

    async def delete_user_acl(self, user_id):
        await self.aclmapper.delete_by_user_id(user_id=user_id)

    async def put_user_acls(self, any_acls: list, pop_acls: list=None, add_acls: list=None):
        for acl in pop_acls or []:
            await self.aclmapper.remove_acl(acls=any_acls, removing_acl=acl)
        if add_acls:
            await self.aclmapper.add_acls(acls=any_acls, adding_acls=add_acls)

    async def put_api_acl(self, method: str, path: str, pop_acls: list=None, add_acls: list=None):
        if not await self.apiaclmapper.select_unique(method=method, path=path):
            await self.apiaclmapper.insert_acl(id=make_unique_id(), method=method, path=path, acl=[])
        for acl in pop_acls or []:
            await self.apiaclmapper.remove_acl_unique(method=method, path=path, removing_acl=acl)
        if add_acls:
            await self.apiaclmapper.add_acls_unique(method=method, path=path, adding_acls=add_acls)

    async def delete_api_acl(self, method: str, path: str):
        await self.delete_api_acl(method=method, path=path)

    async def put_api_acls(self, any_acls: list, pop_acls: list=None, add_acls: list=None):
        for acl in pop_acls or []:
            await self.apiaclmapper.remove_acl(acls=any_acls, removing_acl=acl)
        if add_acls:
            await self.apiaclmapper.add_acls(acls=any_acls, adding_acls=add_acls)
