class AssetNotResolvableException(Exception):

    def __init__(self, message: str):
        super(AssetNotResolvableException, self).__init__(message)
