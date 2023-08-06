from Asset import Asset
from Player import Player

class Client:
    def __init__(self):
        pass

    def FetchAsset(self, id):
        """
        Creates an instance of an Asset class using the given ID
        """
        TypeErrorCheck = isinstance(id, str)
        if TypeErrorCheck:
            raise TypeError(f"Asset ID ({id}) must be in integer form")

        asset_obj = Asset(id=id)
        asset_obj.fetchData()
        return asset_obj
    
    def FetchUser(self, id):
        """
        Creates an instance of a Player class using the given ID
        """
        TypeErrorCheck = isinstance(id, str)
        if TypeErrorCheck:
            raise TypeError(f"User ID ({id}) must be in integer form")

        player_obj = Player(id=id)
        player_obj.fetchData()
        return player_obj