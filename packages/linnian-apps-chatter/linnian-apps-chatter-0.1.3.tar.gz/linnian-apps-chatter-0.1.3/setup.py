# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['linnian', 'linnian.apps.chatter']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0', 'ujson>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'linnian-apps-chatter',
    'version': '0.1.3',
    'description': 'qwq',
    'long_description': None,
    'author': 'LinNian',
    'author_email': '2544704967@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
