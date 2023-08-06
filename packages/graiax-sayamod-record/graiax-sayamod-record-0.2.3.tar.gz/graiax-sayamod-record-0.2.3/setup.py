# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graiax_sayamod_record', 'graiax_sayamod_record.databases']

package_data = \
{'': ['*']}

install_requires = \
['graia-application-mirai==0.16.1',
 'graia-broadcast>=0.7.0,<0.8.0',
 'graia-saya>=0.0.8,<0.0.9',
 'pony>=0.7.14,<0.8.0']

setup_kwargs = {
    'name': 'graiax-sayamod-record',
    'version': '0.2.3',
    'description': 'A graiax saya mod to record message in databases.',
    'long_description': None,
    'author': 'hans',
    'author_email': 'dxzenghan@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
