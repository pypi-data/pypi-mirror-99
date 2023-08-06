# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qctrlcommons', 'qctrlcommons.node']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'dataclasses>=0.6,<0.7',
 'inflection>=0.5.1,<0.6.0',
 'numpy>=1.16.2',
 'pyjwt>=2.0.1,<3.0.0',
 'python-forge>=18.6.0,<19.0.0',
 'pythonflow>=0.3.0,<0.4.0',
 'scipy>=1.4.1',
 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'qctrl-commons',
    'version': '5.2.0',
    'description': 'Q-CTRL Python Commons',
    'long_description': '# Q-CTRL Python Commons\n\nQ-CTRL Python Commons is a collection of common libraries for the Python language.\n',
    'author': 'Q-CTRL',
    'author_email': 'support@q-ctrl.com',
    'maintainer': 'Q-CTRL',
    'maintainer_email': 'support@q-ctrl.com',
    'url': 'https://q-ctrl.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.4,<3.9',
}


setup(**setup_kwargs)
