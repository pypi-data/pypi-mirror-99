import aiohttp
import asyncio

class asyncuserdata():
    def __init__(self, user: str, json: dict):
        self.user = user
        self.json = json
    @classmethod
    async def lookup(self, address: str):
        header={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        async with aiohttp.ClientSession(headers=header) as session:
            async with session.get("https://playerdb.co/api/player/minecraft/{0}".format(address)) as res:
                name = await res.json()

        return asyncuserdata(user=name['data']['player']['username'], json=name)
    async def checkuser(self):
        return self.json
    async def getuser(self, nick: str):
        name = self.json
        return name
    async def username(self):
        gets = await self.getuser(self.user)
        return str(gets['data']['player']['username'])
    async def userid(self):
        gets = await self.getuser(self.user)
        return str(gets['data']['player']['id'])
    async def useravatar(self):
        gets = await self.getuser(self.user)
        return str(gets['data']['player']['avatar'])
    async def userrawid(self):
        gets = await self.getuser(self.user)
        return str(gets['data']['player']['raw_id'])
    