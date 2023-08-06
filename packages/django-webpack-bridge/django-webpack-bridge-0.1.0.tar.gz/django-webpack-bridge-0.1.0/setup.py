# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['templatetags',
 'webpack_bridge',
 'webpack_bridge.templatetags',
 'webpack_bridge.tests']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.0.0']

setup_kwargs = {
    'name': 'django-webpack-bridge',
    'version': '0.1.0',
    'description': 'A bridge from Webpack to Django',
    'long_description': '# Django Webpack Bridge\n\n[![Test, Publish](https://github.com/uw-it-aca/django-webpack-bridge/actions/workflows/cicd.yml/badge.svg)](https://github.com/uw-it-aca/django-webpack-bridge/actions/workflows/cicd.yml)\n\nCreates a bridge from webpack to django.\n\n## Supported Versions\n\nDjango >= 2.1\nWebpack >= 4.44.2\n\n## How to Use\n\n1. Add the packages to `setup.py` and `package.json`.\n   1. Unimplemented: Add `django-webpack-bridge` to install from public registries.\n   2. To install from git\n      1. python: `\'django-webpack-bridge @ https://github.com/uw-it-aca/django-webpack-bridge/tarball/master\'`\n      2. nodejs: `"django-webpack-bridge": "https://github.com/uw-it-aca/django-webpack-bridge.git"`\n2. Add the plugin to `webpack.config.js`\n\n    ```js\n    const DjangoBridgePlugin = require(\'django-webpack-bridge\');\n    module.exports = {\n        ...,\n        plugins: [\n            ...,\n            new DjangoBridgePlugin(),\n        ],\n    }\n    ```\n\n    `django-webpack-bridge` will use the variables from `module.exports.output`\n3. Add the following to `settings.py`\n\n    ```python\n    INSTALLED_APPS += [\n        \'webpack_bridge\',\n    ]\n    STATICFILES_DIRS = [\n        \'{same as module.exports.output.path from webpack.config.js}\',\n    ]\n    ```\n\n4. In the `template.html`\n\n    ```jsx\n    {% load webpack_bridge %}\n    {% render_webpack_entry \'entry point name\' js=\'defer\' %}\n    ```\n\n## Settings\n\n```python\nBRIDGE_SETTINGS = {\n    # Name of the manifest file\n    \'manifest_file\': \'manifest.json\',\n    # Boolean to turn caching on and off\n    \'cache\': not settings.DEBUG,\n    # Timeout duration for the cache\n    \'cache_timeout\': 86400,  # 1 Day\n    # Namespace for the cache\n    \'cache_prefix\': \'webpack_manifest\',\n    # Maps a tag group to a group of tags\n    \'group_to_extensions\': {\n        \'script\': (\'js\', ),\n        \'style\': (\'css\', ),\n    },\n    # Maps a tag group to a html tag\n    \'group_to_html_tag\': {\n        \'script\': \'<script src="{path}" {attributes}></script>\',\n        \'style\':\n            \'<link rel="stylesheet" type="text/css"\'\n            + \' href="{path}" {attributes}>\',\n    },\n    # Time between updaing the manifest from the file while compiling\n    \'compiling_poll_duration\': 0.5,\n}\n```\n\n`group_to_extensions` and `group_to_html_tag` combine to create a multi-key map from a group of file extensions to a html tag. Eg. `(js, jsx) -> <script src="{path}" {attributes}></script>`\n\n`path`: Will be replaced with the bundle path\n`attributes`: Will be replaced with any attributes specfied when when calling \'render_webpack_entry\'. Attributes are grouped by file extension\n\nThe following settings can be passed to `DjangoBridgePlugin`\n\n```js\n{\n    path: \'defaults to module.exports.output.path\',\n    publicPath: \'defaults to module.exports.output.publicPath\',\n    fileName: \'defaults to manifest.json\',\n}\n```\n\n## Development\n\n### Running tests\n\n1. Create and activate a python virtual env of your choice (optional).\n2. Run `pip install .`\n3. Run `DJANGO_SETTINGS_MODULE=test_files.settings python -m django test webpack_bridge`\n\n### Running the Demo\n\n1. Run `docker-compose up --build`\n2. Open `localhost:8000`\n',
    'author': 'UW-IT AXDD',
    'author_email': 'aca-it@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uw-it-aca/django-webpack-bridge',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
