class Exc(Exception):
    pass

class AssetNotFound(Exc):
    """Thrown when asset cannot be located"""

class PlayerNotFound(Exc):
    """Thrown when player cannot be located"""
