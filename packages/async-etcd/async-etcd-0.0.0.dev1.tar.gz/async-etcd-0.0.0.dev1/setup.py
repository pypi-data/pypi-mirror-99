# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['etcd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'async-etcd',
    'version': '0.0.0.dev1',
    'description': 'Asyncio based etcd-v3 client',
    'long_description': '# async-etcd\nAsyncio based etcd-v3 client\n\n## Tagging and publishing\n\nEach push to `master` will make the CI create a development tag as `X.Y.Z.devW` and will build and push the build to pypi. Whenever a non-development version needs to be created, then do the following:\n1. locally run `make bump-{patch|minor|major}`,\n2. open a PR,\n3. merge to `master`\n\nThe CI will detect the new untagged version and will create the corresponding tag and publish to build to pypi.\n',
    'author': 'Lou Marvin Caraig',
    'author_email': 'loumarvincaraig@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/se7entyse7en/async-etcd',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
