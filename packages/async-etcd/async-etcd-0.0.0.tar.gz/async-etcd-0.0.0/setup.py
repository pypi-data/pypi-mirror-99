# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['etcd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'async-etcd',
    'version': '0.0.0',
    'description': 'Asyncio based etcd-v3 client',
    'long_description': '# async-etcd\nAsyncio based etcd-v3 client\n',
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
