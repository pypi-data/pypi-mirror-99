# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boo', 'boo.dataframe', 'boo.okved']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'pandas==1.1.5',
 'requests>=2.25.1,<3.0.0',
 'tqdm>=4.59.0,<5.0.0']

setup_kwargs = {
    'name': 'boo',
    'version': '0.2.0',
    'description': 'Russian corporate financial reports 2012-2018.',
    'long_description': None,
    'author': 'Evgeniy Pogrebnyak',
    'author_email': 'e.pogrebnyak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
