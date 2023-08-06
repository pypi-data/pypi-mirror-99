import logging

from pathlib import Path
from typing import List

import requests
import yaml

from web_asset_vendor.models.asset import Asset
from web_asset_vendor.models.resolver import Resolver
from web_asset_vendor.utils.exceptions import AssetNotResolvableException


class Fetcher:

    logger = logging.getLogger("Fetcher")

    def __init__(self, output: str, resolvers: List[Resolver], assets: List[Asset]):
        self.output = output
        self.resolvers = resolvers
        self.assets = assets

    @classmethod
    def from_yaml(cls, file_path: str):

        with open(file_path) as f:
            data = yaml.load(f, Loader=yaml.BaseLoader)

        output = data['config'].get("output", "vendor").strip("/")
        cls.logger.debug(f"config.output: {output}")

        resolvers = [Resolver.from_dict(res) for res in data['config']['resolvers']]
        cls.logger.debug(f"config.resolver.length: {len(resolvers)}")

        assets = [Asset.from_dict(asset, data['assets'][asset]) for asset in data['assets']]
        cls.logger.debug(f"config.assets.length: {len(assets)}")

        return cls(output, resolvers, assets)

    def fetch(self):

        for asset in self.assets:

            urls: List[str] = []

            for resolver in self.resolvers:
                if not resolver.match_tags(asset.tags):
                    continue

                try:
                    urls.append(resolver.resolve(asset.attributes))

                except AssetNotResolvableException as ex:
                    self.logger.debug(f"missing resolver variable: {str(ex)}")
                    continue

            if len(urls) == 0:
                self.logger.error(f"asset {asset.name} has no resolver")
            else:
                self.logger.debug(f"asset {asset.name} has {len(urls)} potential resolver urls")

            downloaded: bool = False
            for url in urls:

                r = requests.get(url)
                if r.status_code == 200:
                    downloaded = True
                    path = self.output + "/" + asset.folder

                    Path(path).mkdir(parents=True, exist_ok=True)
                    open(f"{path}/{asset.name}", 'wb').write(r.content)

                    break

            if not downloaded:
                self.logger.error(f"failed downloading {asset.name} for all urls")
