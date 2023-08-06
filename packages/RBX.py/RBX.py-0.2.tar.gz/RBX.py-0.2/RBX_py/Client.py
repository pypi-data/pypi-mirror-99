from Asset import Asset

class Client:
    def __init__(self):
        pass

    def FetchAsset(self, id):
        """
        Creates an instance of an Asset class using the given ID
        """
        TypeErrorCheck = isinstance(id, str)
        if TypeErrorCheck:
            raise TypeError(f"Asset ID ({Asset_id}) must be in integer form")

        asset_obj = Asset(id=id)
        asset_obj.fetchData()
        return asset_obj

c = Client()
e = c.FetchAsset(456225312)
print(e.Name)