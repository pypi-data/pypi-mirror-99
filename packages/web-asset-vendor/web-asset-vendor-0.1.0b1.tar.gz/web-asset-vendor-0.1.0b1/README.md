# web-asset-vendor

Downloading assets from the web in a reproducible way.

Intentionally this was used to fetch web-dev assets like .js ans .css files from cdn's but the generic resolver pattern allows you to download everything you want (images, binarys, ...).

## Example Usage

### `main.py`
```python
from web_asset_vendor import Fetcher
fetcher = Fetcher.from_yaml("dependencies.yaml")
fetcher.fetch()
```
Note: Optionally one will not simply initialize Fetcher with a yaml file. Instead, one would use the Constructor.

### `dependencies.yaml`
```yaml
config:
  output: vendor/
  fixiation: True  # WIP
  resolvers:

    # CLOUDFLARE
    - url: https://cdnjs.cloudflare.com/ajax/libs/${author}/${version}/js/${package}.min.js
    - url: https://cdnjs.cloudflare.com/ajax/libs/${author}/${version}/css/${package}.min.css
      tags: [ css ]

    # UNPKG
    - url: https://unpkg.com/${package}@${version}/dist/${package}.min.js
    - url: https://unpkg.com/${package}@${version}/dist/css/${package}.min.css
      tags: [ css ]

assets:
  bootstrap.min.css:
    folder: css/bootstrap
    resolveWith: [ css ]
    resolvedBy:
      author: twitter-bootstrap
      version: 4.6.0
      package: bootstrap

  bootstrap.min.js:
    folder: js/bootstrap
    resolvedBy:
      author: twitter-bootstrap
      version: 4.6.0
      package: bootstrap

  jquery.min.js:
    resolvedBy:
      version: 3.6.0
      package: jquery
```

### example output:
```
.
+-- vendor
|   +-- css
|   |   +-- bootstrap
|   |   |   +-- bootstrap.min.css
|   +-- js
|   |   +-- bootstrap
|   |   |   +-- bootstrap.min.js
|   +-- uncategorized
|   |   +-- jquery.min.css
```
