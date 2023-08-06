import requests

class userdata():
    def __init__(self, user: str, json: dict):
        self.user = user
        self.json = json
    @classmethod
    def lookup(self, address: str):
        name = requests.get("https://playerdb.co/api/player/minecraft/{0}".format(address)).json()
        return userdata(user=name['data']['player']['username'], json=name)
    def checkuser(self):
        return self.json
    def getuser(self, nick: str):
        #name = requests.get("https://playerdb.co/api/player/minecraft/{0}".format(nick)).json()
        name = self.json
        return name
    def username(self):
        #await getuser(self.user)
        gets = self.getuser(self.user)
        return str(gets['data']['player']['username'])
    def userid(self):
        gets = self.getuser(self.user)
        return str(gets['data']['player']['id'])
    def useravatar(self):
        gets = self.getuser(self.user)
        return str(gets['data']['player']['avatar'])
    def userrawid(self):
        gets = self.getuser(self.user)
        return str(gets['data']['player']['raw_id'])