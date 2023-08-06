from typing import List, Dict

from web_asset_vendor.utils.exceptions_runtime import AssetInitFailedError


class Asset:
    def __init__(self, name: str, folder: str, tags: List[str], attributes: Dict[str, str]):
        self.name           = name
        self.folder         = folder.strip("/")
        self.tags           = tags
        self.attributes     = attributes

    @classmethod
    def from_dict(cls, name: str, meta_data: Dict):
        """Initialize Asset from a dict config"""
        try:
            folder          = meta_data.pop("folder", "uncategorized")
            resolve_with    = meta_data.pop("resolveWith", None)
            resolve_by      = meta_data.pop("resolvedBy", None)

        except KeyError as err:
            raise AssetInitFailedError(err)

        return cls(name, folder, resolve_with, resolve_by)
