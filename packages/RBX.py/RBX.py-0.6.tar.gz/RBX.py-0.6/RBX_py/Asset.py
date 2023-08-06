import requests
import json

from RBX_py.Utils import asset_types
from RBX_py.Errors import AssetNotFound

class Asset:
    def __init__(self, id):
        self.id = id
        self.AssetData = None
    
    def fetchData(self):
        r = requests.get(f"http://api.roblox.com/Marketplace/ProductInfo?assetId={self.id}")
        r = json.loads(r.text)

        if "AssetId" not in r.keys():
            raise AssetNotFound
        else:
            self.AssetData = r
    
    @property
    def Name(self):
        return self.AssetData["Name"]
    
    @property
    def Description(self):
        return self.AssetData["Description"]
    
    @property
    def Creator(self):
        return self.AssetData["Creator"]
    
    @property
    def AssetType(self):
        type_id = self.AssetData["AssetTypeId"]
        return asset_types[type_id]

    @property
    def Price(self):
        return self.AssetData["PriceInRobux"] if not None else 0
    
    @property
    def CreatedAt(self):
        return self.AssetData["Created"]

    @property
    def LastUpdated(self):
        return self.AssetData["Updated"]
    
    @property
    def IsForSale(self):
        return self.AssetData["IsForSale"]
    
    @property
    def IsLimited(self):
        LimitedState = False
        if self.AssetData["IsLimited"] == True:
            LimitedState = True
        
        if self.AssetData["IsLimitedUnique"] == True:
            LimitedState = True
        
        return LimitedState
    
    @property
    def ID(self):
        return self.AssetData["ProductId"]
    
    def GetAssetImage(self):
        r = f"https://assetgame.roblox.com/Game/Tools/ThumbnailAsset.ashx?aid={self.id}&fmt=png&wd=420&ht=420"
        return r






