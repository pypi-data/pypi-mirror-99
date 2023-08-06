

from mcuser.module1 import asyncuserdata
from mcuser.module2 import userdata

class MCuser():
    def __init__(self, name: str, look):
        self.name = name
        self.look = look
    @classmethod
    def lookup(self, address: str):
        names = userdata.lookup(address)
        name = names.username()
        return MCuser(name=name, look=names)
    def user_check(self):
        
        name = self.look
        
        name = name.checkuser()
        return name
    def user_id(self):
        name = self.look
        nameid = name.userid()
        return nameid
    def user_name(self):
        name = self.look
        nameuser = name.username()
        return nameuser
    def user_avatar(self):
        name = self.look
        nameavatar = name.useravatar()
        return nameavatar
    def user_rawid(self):
        name = self.look
        namerawid = name.userrawid()
        return namerawid
class asyncMCuser():
    def __init__(self, name: str, look):
        self.name = name
        self.look = look
    

    @classmethod
    async def lookup(self, address: str):
        names = await asyncuserdata.lookup(address)
        name = await names.username()
        return asyncMCuser(name=name, look=names)
    async def asyncuser_check(self):
        name = self.look
        name = await name.checkuser()
        return name
    async def asyncuser_id(self):
        name = self.look
        nameid = await name.userid()
        return nameid
    async def asyncuser_name(self):
        name = self.look
        nameuser = await name.username()
        return nameuser
    async def asyncuser_avatar(self):
        name = self.look
        nameavatar = await name.avatar()
        return nameavatar
    async def asyncuser_rawid(self):
        name = self.look
        namerawid = await name.raw_id()
        return namerawid