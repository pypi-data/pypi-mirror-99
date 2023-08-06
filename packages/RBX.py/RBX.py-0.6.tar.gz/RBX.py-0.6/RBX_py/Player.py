import requests
import json

from RBX_py.Errors import PlayerNotFound
from RBX_py.Utils import name_id_data_type

class Player:
    def __init__(self, id):
        self.id = id
        self.PlayerData = None
    
    def fetchData(self):
        r = requests.get(f"https://users.roblox.com/v1/users/{self.id}")
        r = json.loads(r.text)

        if "id" not in r.keys():
            raise PlayerNotFound
        
        self.BasePlayerInfo = r
    
    @property
    def Name(self):
        return self.BasePlayerInfo["name"]
    
    @property
    def Description(self):
        desc = self.BasePlayerInfo["description"]

        if desc == "":
            return None
        else:
            return desc
    
    @property
    def CreatedAt(self):
        return self.BasePlayerInfo["created"]
    
    @property
    def ProfileLink(self):
        return f"https://www.roblox.com/users/{self.id}/profile"
    
    def GetUserIcon(self):
        data = {"size": "720x720", "format": "Png",}
        r = requests.get(url=f"https://thumbnails.roblox.com/v1/users/avatar?userIds={self.id}", params=data)
        r = json.loads(r.text)
        return r["data"][0]["imageUrl"]
    
    def GetUserFriends(self):
        r = requests.get(f"https://friends.roblox.com/v1/users/{self.id}/friends")
        r = json.loads(r.text)

        finalized_friend_data = []

        for friend in r["data"]:
            fr_obj = name_id_data_type(friend["name"], friend["id"])
            finalized_friend_data.append(fr_obj)
            
        return finalized_friend_data
    
    def GetUserGroups(self):
        r = requests.get(f"https://groups.roblox.com/v2/users/{self.id}/groups/roles")
        r = json.loads(r.text)

        finalized_group_data = []

        for group in r["data"]:
            group = group["group"]
            gr_obj = name_id_data_type(group["name"], group["id"])
            finalized_group_data.append(gr_obj)

        if finalized_group_data is []:
            return None
        else:
            return finalized_group_data
    
    def GetFollowerCount(self):
        r = requests.get(f"https://friends.roblox.com/v1/users/{self.id}/followers/count")
        r = json.loads(r.text)

        return r["count"]