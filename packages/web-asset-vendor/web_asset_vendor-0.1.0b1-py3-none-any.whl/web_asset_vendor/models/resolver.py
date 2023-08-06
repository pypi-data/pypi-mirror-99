from typing import List, Dict
from typing.re import Match

from web_asset_vendor.utils.exceptions import AssetNotResolvableException
from web_asset_vendor.utils.exceptions_runtime import ResolverInitFailedError
from web_asset_vendor.utils.regex import RESOLVER_VARIABLES


class Resolver:

    def __init__(self, url: str, tags: List[str]):
        self.url = url
        self.tags = tags

    @classmethod
    def from_dict(cls, datadict: Dict):
        """Initialize Resolver from a dict config"""
        try:
            url = datadict['url']
            tags = datadict.get('tags', None)
        except KeyError as err:
            raise ResolverInitFailedError(err)

        return cls(url, tags)

    def match_tags(self, tags: List[str]) -> bool:
        if tags is None or self.tags is None:
            return tags is None and self.tags is None

        else:
            return len(set(tags).intersection(set(self.tags))) >= len(tags)

    def resolve(self, attributes: Dict[str, str]) -> str:

        matched = set([])

        def _resolve_cb(match_obj: Match):
            if attributes is None:
                raise AssetNotResolvableException("asset has no attributes")

            try:
                matched.add(match_obj.group(1))
                return attributes[match_obj.group(1)]
            except KeyError as ex:
                raise AssetNotResolvableException(ex.args[0])

        resolved_url = RESOLVER_VARIABLES.sub(_resolve_cb, self.url)

        return resolved_url
